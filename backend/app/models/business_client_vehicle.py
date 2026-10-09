from datetime import datetime, timezone

from app.extensions import db


class BusinessClientVehicle(db.Model):
    """Мотоцикл клиента бизнес-аккаунта."""

    __tablename__ = "business_client_vehicles"

    id = db.Column(db.Integer, primary_key=True)
    business_client_id = db.Column(
        db.Integer,
        db.ForeignKey("business_clients.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    name = db.Column(db.String(120), nullable=False)
    years = db.Column(db.Integer)
    volume = db.Column(db.Integer)
    mileage = db.Column(db.Integer, default=0)
    vin = db.Column(db.String(64), index=True)
    license_plate = db.Column(db.String(20))
    color = db.Column(db.String(16), default="#FFFFFF")
    note = db.Column(db.Text)

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
    client = db.relationship("BusinessClient", back_populates="vehicles")

    def to_dict(self):
        return {
            "id": self.id,
            "business_client_id": self.business_client_id,
            "name": self.name,
            "years": self.years,
            "volume": self.volume,
            "mileage": self.mileage,
            "vin": self.vin,
            "license_plate": self.license_plate,
            "color": self.color,
            "note": self.note,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
