from datetime import datetime, timezone

from app.extensions import db


class SlotAdjustment(db.Model):
    """Append-only audit record for manually gifted garage slots."""

    __tablename__ = "slot_adjustments"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    user_email = db.Column(db.String(128), nullable=False)
    admin_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    admin_email = db.Column(db.String(128), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    reason = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc), index=True)

    user = db.relationship("User", foreign_keys=[user_id])
    admin = db.relationship("User", foreign_keys=[admin_id])

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "user_email": self.user_email,
            "admin_id": self.admin_id,
            "admin_email": self.admin_email,
            "quantity": self.quantity,
            "reason": self.reason,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
