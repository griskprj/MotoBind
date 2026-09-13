from datetime import datetime, timezone
from app.extensions import db


class Reminder(db.Model):
    """
    Напоминание пользователю.
    """
    __tablename__ = "reminders"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    motorcycle_id = db.Column(
        db.Integer,
        db.ForeignKey("motorcycles.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    maintenance_id = db.Column(
        db.Integer,
        db.ForeignKey("maintenances.id", ondelete="CASCADE"),
        nullable=True,
        index=True
    )

    type = db.Column(db.String(32), nullable=False, index=True)
    status = db.Column(db.String(16), nullable=False, default="pending", index=True)

    last_sent_at = db.Column(db.DateTime, nullable=True)
    next_send_at = db.Column(db.DateTime, nullable=True)

    snoozed_until = db.Column(db.DateTime, nullable=True)

    dismissed_at = db.Column(db.DateTime, nullable=True)

    created_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    user = db.relationship(
        "User",
        back_populates="reminders",
        foreign_keys=[user_id],
    )
    motorcycle = db.relationship(
        "Motorcycle",
        back_populates="reminders",
        foreign_keys=[motorcycle_id],
    )
    maintenance = db.relationship(
        "Maintenance",
        foreign_keys=[maintenance_id],
    )

    TYPE_MILEAGE_UPDATE = "mileage_update"
    TYPE_MAINTENANCE_SOON = "maintenance_soon"
    TYPE_MAINTENANCE_OVERDUE = "maintenance_overdue"

    TYPE_LABELS = {
        TYPE_MILEAGE_UPDATE: "Обновление пробега",
        TYPE_MAINTENANCE_SOON: "Скоро ТО",
        TYPE_MAINTENANCE_OVERDUE: "Просрочено ТО"
    }

    STATUS_PENDING = "pending"
    STATUS_DISMISSED = "dismissed"

    __table_args__ = (
        db.Index("ix_reminders_status_next_send", "status", "next_send_at"),
        db.Index("ix_reminders_user_status", "user_id", "status")
    )

    def to_dict(self, include_moto=False):
        data = {
            "id": self.id,
            "user_id": self.user_id,
            "motorcycle_id": self.motorcycle_id,
            "maintenance_id": self.maintenance_id,
            "type": self.type,
            "type_label": self.TYPE_LABELS.get(self.type, self.type),
            "status": self.status,
            "last_sent_at": self.last_sent_at.isoformat() if self.last_sent_at else None,
            "next_send_at": self.next_send_at.isoformat() if self.next_send_at else None,
            "snoozed_until": self.snoozed_until.isoformat() if self.snoozed_until else None,
            "dismissed_at": self.dismissed_at.isoformat() if self.dismissed_at else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

        if include_moto and self.motorcycle:
            data["motorcycle"] = {
                "id": self.motorcycle.id,
                "name": self.motorcycle.name,
                "mileage": self.motorcycle.mileage
            }

        return data