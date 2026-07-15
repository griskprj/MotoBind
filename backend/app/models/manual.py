from datetime import datetime, timezone
from app.extensions import db


class Manual(db.Model):
    """ Модель мануала по ремонту """
    __tablename__ = 'manuals'

    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(64), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(32), nullable=False)
    difficult = db.Column(db.String(32), default='easy')
    instruments = db.Column(db.Text)
    parts = db.Column(db.Text)
    motorcycle = db.Column(db.String(64), nullable=False)
    status = db.Column(db.String(32), default='moderate')
    rejection_reason = db.Column(db.String(32), default='')
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    
    author = db.relationship('User', backref='manuals')
    steps = db.relationship('ManualStep', lazy='select', cascade='all, delete-orphan')

    def to_dict(self):
        """ Сеарилизация данных """
        return {
            'id': self.id,
            'author_id': self.author_id,
            'author_username': self.author.username,
            'title': self.title,
            'description': self.description,
            'category': self.category,
            'difficult': self.difficult,
            'instruments': self.instruments,
            'parts': self.parts,
            'motorcycle': self.motorcycle,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'steps': [s.to_dict() for s in self.steps]
        }

class ManualStep(db.Model):
    """ Модель шага мануала """

    __tablename__ = 'manual_steps'
    id = db.Column(db.Integer, primary_key=True)
    manual_id = db.Column(db.Integer, db.ForeignKey('manuals.id'), nullable=False)
    order = db.Column(db.Integer, default=0, nullable=False)
    title = db.Column(db.String(64), nullable=False)
    text = db.Column(db.Text)

    def to_dict(self):
        return {
            'id': self.id,
            'manual_id': self.manual_id,
            'order': self.order,
            'title': self.title,
            'text': self.text
        }

