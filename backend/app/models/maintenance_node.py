from app.extensions import db


class MaintenanceNode(db.Model):
    """Модель узла обслуживания"""

    id = db.Column(db.Integer, primary_key=True)
    moto_id = db.Column(db.Integer, db.ForeignKey("motorcycles.id"), nullable=False)
    title = db.Column(db.String(32), nullable=False)
    category = db.Column(db.String(32))

    def to_dict(self):
        return {
            "id": self.id,
            "moto_id": self.moto_id,
            "title": self.title,
            "category": self.category,
        }
