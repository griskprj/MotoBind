from app.extensions import db


class Manual(db.Model):
    """ Модель мануала по ремонту """
    __tablename__ = 'manuals'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(32), nullable=False)
    type = db.Column(db.String(32), nullable=False)
    difficult = db.Column(db.String(32), default='easy')
    instruments = db.Column(db.Text)
    parts = db.Column(db.Text)

    motorcycle = db.Column(db.String(64), nullable=False)

    steps = db.relationship('ManualStep', lazy='select', cascade='all, delete-orphan')

class ManualStep(db.Model):
    """ Модель шага мануала """

    __tablename__ = 'manual_steps'
    id = db.Column(db.Integer, primary_key=True)
    manual_id = db.Column(db.Integer, db.ForeignKey('manuals.id'))
    order = db.Column(db.Integer, default=0, nullable=False)
    title = db.Column(db.String(64), nullable=False)
    text = db.Column(db.Text)