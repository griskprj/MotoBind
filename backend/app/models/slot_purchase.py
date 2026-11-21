from datetime import datetime, timezone

from app.extensions import db


class SlotPurchase(db.Model):
    """Payment order for one additional motorcycle slot."""

    __tablename__ = "slot_purchases"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False,
        index=True,
    )
    amount = db.Column(db.Integer, nullable=False, default=49)
    status = db.Column(db.String(20), nullable=False, default="pending", index=True)
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    paid_at = db.Column(db.DateTime, nullable=True)
    refunded_at = db.Column(db.DateTime, nullable=True)
    refund_reason = db.Column(db.String(500), nullable=True)
    refunded_by = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    refunded_by_email = db.Column(db.String(128), nullable=True)
    refund_reference = db.Column(db.String(128), nullable=True)

    user = db.relationship("User", back_populates="slot_purchases", foreign_keys=[user_id])

    def to_admin_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "username": self.user.username if self.user else None,
            "email": self.user.email if self.user else None,
            "amount": self.amount,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "paid_at": self.paid_at.isoformat() if self.paid_at else None,
            "refunded_at": self.refunded_at.isoformat() if self.refunded_at else None,
            "refund_reason": self.refund_reason,
            "refunded_by": self.refunded_by,
            "refunded_by_email": self.refunded_by_email,
            "refund_reference": self.refund_reference,
        }
