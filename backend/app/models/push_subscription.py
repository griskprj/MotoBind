from datetime import datetime, timezone

from app.extensions import db


class PushSubscription(db.Model):
    """A browser endpoint that can receive Web Push for one user."""

    __tablename__ = "push_subscriptions"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    endpoint = db.Column(db.String(2048), nullable=False, unique=True)
    p256dh = db.Column(db.String(256), nullable=False)
    auth = db.Column(db.String(128), nullable=False)
    created_at = db.Column(
        db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc)
    )
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    user = db.relationship("User", back_populates="push_subscriptions")
