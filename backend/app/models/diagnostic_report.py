from datetime import datetime, timezone

from app.extensions import db


class DiagnosticReport(db.Model):
    """
    Сохранённый отчёт онлайн-диагностики.

    results хранит только [{rule_id, score}] — тексты причин
    подтягиваются из RULES на фронте при просмотре отчёта.
    """

    __tablename__ = "diagnostic_reports"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False, index=True
    )
    motorcycle_id = db.Column(
        db.Integer, db.ForeignKey("motorcycles.id"), nullable=True, index=True
    )
    mileage = db.Column(db.Integer, nullable=True)
    locked_group = db.Column(db.String(32), nullable=True)

    symptoms = db.Column(db.JSON, nullable=False, default=list)
    answers = db.Column(db.JSON, nullable=False, default=dict)
    results = db.Column(db.JSON, nullable=False, default=list)

    created_at = db.Column(
        db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
    )

    user = db.relationship("User", backref="diagnostic_reports")
    motorcycle = db.relationship("Motorcycle", backref="diagnostic_reports")

    __table_args__ = (
        db.Index("idx_diag_user_created", "user_id", "created_at"),
        db.Index("idx_diag_moto", "motorcycle_id"),
    )

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "motorcycle_id": self.motorcycle_id,
            "mileage": self.mileage,
            "locked_group": self.locked_group,
            "symptoms": self.symptoms or [],
            "answers": self.answers or {},
            "results": self.results or [],
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
