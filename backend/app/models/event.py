from datetime import datetime, timezone
from app.extensions import db

event_subscriptions = db.Table('event_subscriptions',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('event_id', db.Integer, db.ForeignKey('events.id'), primary_key=True)
)

class Event(db.Model):
    """ Модель мероприятия """
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(64), nullable=False)
    description = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    status = db.Column(db.String(16), default='moderate', nullable=False)

    subscriptions = db.relationship('User', 
        secondary=event_subscriptions,
        backref='subscribed_events',
        lazy='select')

    def to_dict(self, include_subscriptions: bool) -> dict:
        """ Сериализация данных """
        result = {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'date': self.date.isoformat() if self.date else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'status': self.status
        }

        if include_subscriptions:
            result['subscriptions'] = [s.to_dict() for s in self.subscriptions]
        
        return result