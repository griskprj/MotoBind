from datetime import datetime, timezone

from app.extensions import db


class BookingStatus:
    PENDING = "pending"
    CONFIRMED = "confirmed"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    DECLINED = "declined"


class ServiceBooking(db.Model):
    """Заявка клиента к мастеру/СТО на услугу."""

    __tablename__ = "service_bookings"

    id = db.Column(db.Integer, primary_key=True)

    client_user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    business_account_id = db.Column(
        db.Integer,
        db.ForeignKey("business_accounts.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    service_id = db.Column(
        db.Integer,
        db.ForeignKey("services.id", ondelete="SET NULL"),
        nullable=True,
    )

    motorcycle_id = db.Column(
        db.Integer,
        db.ForeignKey("motorcycles.id", ondelete="SET NULL"),
        nullable=True,
    )

    status = db.Column(
        db.String(16),
        default=BookingStatus.PENDING,
        nullable=False,
        index=True,
    )

    scheduled_at = db.Column(db.DateTime, nullable=False, index=True)
    completed_at = db.Column(db.DateTime)
    cancelled_at = db.Column(db.DateTime)

    client_note = db.Column(db.Text)
    master_note = db.Column(db.Text)
    cancel_reason = db.Column(db.String(256))

    price_final = db.Column(db.Integer)

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
    client = db.relationship("User", foreign_keys=[client_user_id])
    business_account = db.relationship("BusinessAccount")
    service = db.relationship("Service")
    motorcycle = db.relationship("Motorcycle", foreign_keys=[motorcycle_id])

    def to_dict(self, include_relations: bool = False):
        data = {
            "id": self.id,
            "client_user_id": self.client_user_id,
            "business_account_id": self.business_account_id,
            "service_id": self.service_id,
            "motorcycle_id": self.motorcycle_id,
            "status": self.status,
            "scheduled_at": self.scheduled_at.isoformat()
            if self.scheduled_at
            else None,
            "completed_at": self.completed_at.isoformat()
            if self.completed_at
            else None,
            "cancelled_at": self.cancelled_at.isoformat()
            if self.cancelled_at
            else None,
            "client_note": self.client_note,
            "master_note": self.master_note,
            "cancel_reason": self.cancel_reason,
            "price_final": self.price_final,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

        if include_relations:
            if self.client:
                data["client"] = {
                    "id": self.client.id,
                    "username": self.client.username,
                    "avatar": self.client.avatar,
                }
            if self.business_account:
                data["business"] = {
                    "id": self.business_account.id,
                    "type": self.business_account.type,
                    "name": self.business_account.name,
                    "slug": self.business_account.slug,
                    "logo_url": self.business_account.logo_url,
                    "phone": self.business_account.phone,
                    "city": self.business_account.city,
                }
            if self.service:
                data["service"] = self.service.to_dict()
            if self.motorcycle:
                data["motorcycle"] = self.motorcycle.to_dict()

        return data
