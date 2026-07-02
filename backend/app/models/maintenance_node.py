from app.extensions import db

class MaintenanceNode(db.Model):
    """ Модель узла обслуживания """

    id = db.Column(db.Integer, primary_key=True)
    moto_id = db.Column(db.Integer, db.ForeignKey('motorcycles.id'), nullable=False)
    title = db.Column(db.String(32), nullable=False)
    category = db.Column(db.String(32))