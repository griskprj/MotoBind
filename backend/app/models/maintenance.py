from datetime import datetime, timezone
from app.extensions import db


class Maintenance(db.Model):
    """ Maintenance model """
    __tablename__ = 'maintenances'

    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    moto_id = db.Column(db.Integer, db.ForeignKey('motorcycles.id'), nullable=False)
    title = db.Column(db.String(64), nullable=False)
    description = db.Column(db.Text, nullable=False)
    mileage = db.Column(db.Integer)
    category = db.Column(db.String, nullable=False)
    cost = db.Column(db.Integer, default=0, nullable=False)
    date = db.Column(db.DateTime)
    photo_url = db.Column(db.String(256))
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        """ Serialize data to JSON """
        return {
            'id': self.id,
            'author_id': self.author_id,
            'moto_id': self.moto_id,
            'title': self.title,
            'description': self.description,
            'mileage': self.mileage,
            'category': self.category,
            'cost': self.cost,
            'date': self.date,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

class PlannedMaintenance(db.Model):
    """ Planned maintenance model """
    __tablename__ = 'planned_maintenances'

    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    moto_id = db.Column(db.Integer, db.ForeignKey('motorcycles.id'), nullable=False)
    title = db.Column(db.String(64), nullable=False)
    description = db.Column(db.Text, nullable=False)
    planned_mileage = db.Column(db.Integer)
    category = db.Column(db.String, nullable=False, default='general')
    photo_url = db.Column(db.String(256))
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        """ Serialize data to JSON with auto status check """
        return {
            'id': self.id,
            'author_id': self.author_id,
            'moto_id': self.moto_id,
            'title': self.title,
            'description': self.description,
            'planned_mileage': self.planned_mileage,
            'category': self.category,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
