import json
from urllib.parse import urlparse

from flask import current_app
from pywebpush import WebPushException, webpush

from app.extensions import db
from app.models.push_subscription import PushSubscription


class PushService:
    @staticmethod
    def public_config(user_id: int) -> dict:
        return {
            "configured": bool(
                current_app.config.get("WEBPUSH_VAPID_PUBLIC_KEY")
                and current_app.config.get("WEBPUSH_VAPID_PRIVATE_KEY")
            ),
            "public_key": current_app.config.get("WEBPUSH_VAPID_PUBLIC_KEY") or None,
            "enabled": PushSubscription.query.filter_by(user_id=user_id).count() > 0,
        }

    @staticmethod
    def save_subscription(user_id: int, data: dict) -> PushSubscription:
        endpoint = str(data.get("endpoint", "")).strip()
        keys = data.get("keys") if isinstance(data.get("keys"), dict) else {}
        p256dh = str(keys.get("p256dh", "")).strip()
        auth = str(keys.get("auth", "")).strip()
        endpoint_host = urlparse(endpoint).hostname or ""
        allowed_endpoint = (
            endpoint_host == "fcm.googleapis.com"
            or endpoint_host == "web.push.apple.com"
            or endpoint_host.endswith(".push.services.mozilla.com")
            or endpoint_host.endswith(".notify.windows.com")
        )
        if (
            not endpoint.startswith("https://")
            or not allowed_endpoint
            or len(endpoint) > 2048
            or not p256dh
            or len(p256dh) > 256
            or not auth
            or len(auth) > 128
        ):
            from app.exceptions import ValidationError
            raise ValidationError("Некорректная push-подписка")

        subscription = PushSubscription.query.filter_by(endpoint=endpoint).first()
        if subscription is None:
            subscription = PushSubscription(user_id=user_id, endpoint=endpoint)
            db.session.add(subscription)
        subscription.user_id = user_id
        subscription.p256dh = p256dh
        subscription.auth = auth
        db.session.commit()
        return subscription

    @staticmethod
    def remove_subscription(user_id: int, endpoint: str | None = None) -> int:
        query = PushSubscription.query.filter_by(user_id=user_id)
        if endpoint:
            query = query.filter_by(endpoint=endpoint)
        removed = query.delete(synchronize_session=False)
        db.session.commit()
        return removed

    @staticmethod
    def send_to_user(user_id: int, title: str, body: str, link: str | None = None) -> None:
        private_key = current_app.config.get("WEBPUSH_VAPID_PRIVATE_KEY")
        subject = current_app.config.get("WEBPUSH_VAPID_SUBJECT")
        if not private_key or not current_app.config.get("WEBPUSH_VAPID_PUBLIC_KEY"):
            return

        subscriptions = PushSubscription.query.filter_by(user_id=user_id).all()
        for subscription in subscriptions:
            try:
                webpush(
                    subscription_info={
                        "endpoint": subscription.endpoint,
                        "keys": {"p256dh": subscription.p256dh, "auth": subscription.auth},
                    },
                    data=json.dumps(
                        {
                            "title": title[:120],
                            "body": body[:300],
                            "url": link or "/notifications",
                        },
                        ensure_ascii=False,
                    ),
                    vapid_private_key=private_key,
                    vapid_claims={"sub": subject},
                    ttl=60 * 60 * 24,
                    timeout=8,
                )
            except WebPushException as error:
                response = getattr(error, "response", None)
                status_code = getattr(response, "status_code", None)
                if status_code in {404, 410}:
                    db.session.delete(subscription)
                    db.session.commit()
                else:
                    current_app.logger.warning(
                        "Web Push delivery failed for subscription %s (HTTP %s)",
                        subscription.id,
                        status_code,
                    )
            except Exception:
                current_app.logger.exception(
                    "Unexpected Web Push delivery failure for subscription %s",
                    subscription.id,
                )
