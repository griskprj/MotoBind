from datetime import datetime, timezone
from app.extensions import db


class Motorcycle(db.Model):
    """ Motorcycle model """
    __tablename__ = 'motorcycles'

    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(64), nullable=False)
    years = db.Column(db.Integer)
    volume = db.Column(db.Integer)
    mileage = db.Column(db.Integer, default=0)
    color = db.Column(db.String(16), default='#FFFFFF')
    license_plate = db.Column(db.String(10))
    vin = db.Column(db.String(64))
    photo_url = db.Column(db.String(256))
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    maintenances = db.relationship('Maintenance', lazy='select', cascade='all, delete-orphan')
    planned_maintenances = db.relationship('PlannedMaintenance', lazy='select', cascade='all, delete-orphan')

    def to_dict(self, include_maintenance: bool = False, include_planned_maintenance: bool = False):
        """ Serialize data to JSON """
        data = {
            'id': self.id,
            'owner_id': self.owner_id,
            'name': self.name,
            'years': self.years,
            'volume': self.volume,
            'mileage': self.mileage,
            'color': self.color,
            'license_plate': self.license_plate,
            'vin': self.vin,
            'photo_url': self.photo_url,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

        if include_maintenance:
            data['maintenances'] = [m.to_dict() for m in self.maintenance]

        if include_planned_maintenance:
            data['planned_maintenances'] = [m.to_dict() for m in self.planned_maintenances]
        
        return data