from datetime import datetime, timezone
from enum import Enum

from app.extensions import db

class MaintenanceStatus(Enum):
    PLANNED = "planned"
    COMPLETED = "completed"
    OVERDUE = "overdue"

class Maintenance(db.Model):
    __tablename__ = "maintenances"

    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    moto_id = db.Column(db.Integer, db.ForeignKey("motorcycles.id"), nullable=False)
    category = db.Column(db.String, nullable=False)
    title = db.Column(db.String(64), nullable=False)
    description = db.Column(db.Text, nullable=False)
    planned_mileage = db.Column(db.Integer, default=None)
    planned_date = db.Column(db.Date, default=None)
    completed_mileage = db.Column(db.Integer, default=None)
    completed_date = db.Column(db.Date, default=None)
    cost = db.Column(db.Integer, default=0, nullable=False)
    status = db.Column(db.String(16), default=MaintenanceStatus.PLANNED)
    photo_url = db.Column(db.String(256))
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    __table_args__ = (
        db.Index("idx_maintenance_moto_id", "moto_id"),
        db.Index("idx_maintenance_status", "status")
    )

    def to_dict(self):
        return {
            "id": self.id,
            "author_id": self.author_id,
            "moto_id": self.moto_id,
            "category": self.category,
            "title": self.title,
            "description": self.description,
            "planned_mileage": self.planned_mileage,
            "planned_date": self.planned_date.isoformat() if self.planned_date else None,
            "completed_mileage": self.completed_mileage,
            "completed_date": self.completed_date.isoformat() if self.completed_date else None,
            "cost": self.cost,
            "status": self.status if self.status else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }