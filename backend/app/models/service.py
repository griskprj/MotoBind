from datetime import datetime, timezone

from app.extensions import db


class ServiceStatus:
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


class ServiceCategory:
    MAINTENANCE = "maintenance"
    REPAIR = "repair"
    DIAGNOSTICS = "diagnostics"
    TUNING = "tuning"
    OTHER = "other"


class Service(db.Model):
    """Услуга мастера или СТО. Проходит ручную модерацию."""

    __tablename__ = "services"

    id = db.Column(db.Integer, primary_key=True)

    business_account_id = db.Column(
        db.Integer,
        db.ForeignKey("business_accounts.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(
        db.String(32),
        nullable=False,
        default=ServiceCategory.OTHER,
        index=True,
    )

    price_from = db.Column(db.Integer)
    price_to = db.Column(db.Integer)
    duration_min = db.Column(db.Integer)

    status = db.Column(
        db.String(16),
        default=ServiceStatus.PENDING,
        nullable=False,
        index=True,
    )
    rejection_reason = db.Column(db.String(256))

    created_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # relationships
    business_account = db.relationship("BusinessAccount")

    def to_dict(self):
        return {
            "id": self.id,
            "business_account_id": self.business_account_id,
            "title": self.title,
            "description": self.description,
            "category": self.category,
            "price_from": self.price_from,
            "price_to": self.price_to,
            "duration_min": self.duration_min,
            "status": self.status,
            "rejection_reason": self.rejection_reason,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
