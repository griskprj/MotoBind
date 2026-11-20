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

    user = db.relationship("User", back_populates="slot_purchases")
