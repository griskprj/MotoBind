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
    title = db.Column(db.String(64), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String, nullable=False)
    cost = db.Column(db.Integer, default=0, nullable=False)

    completed_mileage = db.Column(db.Integer, default=None)
    planned_mileage = db.Column(db.Integer, default=None)

    completed_date = db.Column(db.Date, default=None)
    planned_date = db.Column(db.Date, default=None)

    status = db.Column(db.String(16), default=MaintenanceStatus.PLANNED)

    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    photo_url = db.Column(db.String(256))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    moto = db.relationship('Motorcycle', back_populates='maintenances')
    author = db.relationship('User', back_populates='maintenances')

    __table_args__ = (
        db.Index("idx_maintenance_moto_id", "moto_id"),
        db.Index("idx_maintenance_status", "status")
    )

    def to_dict(self):
        return {
            'id': self.id,
            'author_id': self.author_id,
            'moto_id': self.moto_id,
            'title': self.title,
            'description': self.description,
            'category': self.category,
            'cost': self.cost,
            'completed_mileage': self.completed_mileage,
            'planned_mileage': self.planned_mileage,
            'completed_date': self.completed_date.isoformat() if self.completed_date else None,
            'planned_date': self.planned_date.isoformat() if self.planned_date else None,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }