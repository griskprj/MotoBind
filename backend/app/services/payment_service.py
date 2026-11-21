import hashlib
import json
import secrets
from decimal import Decimal, InvalidOperation
from urllib.parse import quote, urlencode
from sqlalchemy import func

from flask import current_app

from app.exceptions import APIException, ConflictError, NotFoundError
from app.extensions import db
from app.models.motorcycle import Motorcycle
from app.models.slot_purchase import SlotPurchase
from app.models.slot_adjustment import SlotAdjustment
from app.models.user import User


class PaymentService:
    SLOT_PRICE = 49
    FREE_SLOTS = 1
    ROBOKASSA_URL = "https://auth.robokassa.ru/Merchant/Index.aspx"

    @classmethod
    def _settings(cls):
        cfg = current_app.config
        test_mode = bool(cfg.get("ROBOKASSA_TEST_MODE", True))
        password_1 = cfg.get(
            "ROBOKASSA_TEST_PASSWORD_1" if test_mode else "ROBOKASSA_PASSWORD_1", ""
        )
        password_2 = cfg.get(
            "ROBOKASSA_TEST_PASSWORD_2" if test_mode else "ROBOKASSA_PASSWORD_2", ""
        )
        merchant = cfg.get("ROBOKASSA_MERCHANT_LOGIN", "")
        algorithm = str(cfg.get("ROBOKASSA_HASH_ALGORITHM", "MD5")).upper()
        if not merchant or not password_1 or not password_2:
            raise APIException("Оплата пока не настроена", status_code=503)
        if algorithm not in {"MD5", "SHA256", "SHA1"}:
            raise APIException("Неподдерживаемый алгоритм подписи Robokassa", status_code=503)
        return merchant, password_1, password_2, algorithm, test_mode

    @staticmethod
    def _signature(value: str, algorithm: str) -> str:
        digest = hashlib.new(algorithm.lower())
        digest.update(value.encode("utf-8"))
        return digest.hexdigest()

    @classmethod
    def get_slots(cls, user_id: int) -> dict:
        user = User.query.get_or_404(user_id)
        owned = Motorcycle.query.filter_by(owner_id=user_id).count()
        purchased = SlotPurchase.query.filter_by(user_id=user_id, status="paid").count()
        gifted = db.session.query(func.coalesce(func.sum(SlotAdjustment.quantity), 0)).filter_by(user_id=user_id).scalar()
        legacy_extra = user.extra_motorcycle_slots or 0
        extra = legacy_extra + purchased + gifted
        return {
            "motorcycles_count": owned,
            "free_slots": cls.FREE_SLOTS,
            "purchased_slots": purchased,
            "gifted_slots": gifted,
            "legacy_slots": legacy_extra,
            "slots_total": cls.FREE_SLOTS + extra,
            "slots_available": max(0, cls.FREE_SLOTS + extra - owned),
            "price": cls.SLOT_PRICE,
        }

    @classmethod
    def create_slot_order(cls, user_id: int) -> dict:
        merchant, password_1, _password_2, algorithm, test_mode = cls._settings()
        purchase = SlotPurchase(user_id=user_id, amount=cls.SLOT_PRICE, status="pending")
        db.session.add(purchase)
        db.session.flush()

        out_sum = f"{purchase.amount:.2f}"
        receipt = {
            "items": [{
                "name": "Дополнительное место для мотоцикла MotoBind",
                "quantity": 1,
                "sum": purchase.amount,
                "payment_method": current_app.config.get("ROBOKASSA_PAYMENT_METHOD", "full_payment"),
                "payment_object": current_app.config.get("ROBOKASSA_PAYMENT_OBJECT", "service"),
                "tax": current_app.config.get("ROBOKASSA_TAX", "none"),
            }]
        }
        receipt_json = json.dumps(receipt, ensure_ascii=False, separators=(",", ":"))
        receipt_signature_value = quote(receipt_json, safe="")
        signature = cls._signature(
            f"{merchant}:{out_sum}:{purchase.id}:{receipt_signature_value}:{password_1}",
            algorithm,
        )
        params = {
            "MerchantLogin": merchant,
            "OutSum": out_sum,
            "InvId": str(purchase.id),
            "Description": "Дополнительное место для мотоцикла MotoBind",
            "Email": User.query.get(user_id).email,
            # Robokassa expects the URL-encoded receipt value in the signature;
            # urlencode below encodes this value once more for transport.
            "Receipt": receipt_signature_value,
            "SignatureValue": signature,
        }
        if test_mode:
            params["IsTest"] = "1"
        db.session.commit()
        return {
            "order_id": purchase.id,
            "status": purchase.status,
            "amount": purchase.amount,
            "payment_url": f"{cls.ROBOKASSA_URL}?{urlencode(params)}",
        }

    @staticmethod
    def get_order_status(user_id: int, order_id: int) -> dict:
        purchase = SlotPurchase.query.filter_by(
            id=order_id, user_id=user_id
        ).first()
        if purchase is None:
            raise NotFoundError("Платёжный заказ не найден")
        return {
            "order_id": purchase.id,
            "status": purchase.status,
            "amount": purchase.amount,
            "paid_at": purchase.paid_at.isoformat() if purchase.paid_at else None,
        }

    @classmethod
    def handle_result(cls, data: dict) -> str:
        _merchant, _password_1, password_2, algorithm, _test_mode = cls._settings()
        try:
            invoice_id = int(data.get("InvId", ""))
            amount = Decimal(str(data.get("OutSum", "")))
        except (ValueError, InvalidOperation):
            raise APIException("Некорректные параметры уведомления", status_code=400)
        signature_received = str(data.get("SignatureValue", "")).lower()
        if not signature_received or not data.get("OutSum"):
            raise APIException("В уведомлении отсутствуют обязательные параметры", status_code=400)
        if not amount.is_finite() or amount <= 0:
            raise APIException("Некорректная сумма платежа", status_code=400)

        user_fields = sorted(
            (key, value) for key, value in data.items()
            if key.lower().startswith("shp_")
        )
        signature_source = f"{data['OutSum']}:{invoice_id}:{password_2}"
        for key, value in user_fields:
            signature_source += f":{key}={value}"
        expected = cls._signature(signature_source, algorithm)
        if not secrets.compare_digest(signature_received, expected.lower()):
            raise APIException("Некорректная подпись уведомления", status_code=403)

        purchase = db.session.get(SlotPurchase, invoice_id)
        if purchase is None:
            raise NotFoundError("Платёжный заказ не найден")
        if purchase.amount != amount:
            raise APIException("Сумма или магазин не совпадают с заказом", status_code=400)
        # A retried Robokassa callback must never reactivate a manually refunded order.
        if purchase.status == "pending":
            from datetime import datetime, timezone
            purchase.status = "paid"
            purchase.paid_at = datetime.now(timezone.utc)
            db.session.commit()
        return f"OK{purchase.id}"
