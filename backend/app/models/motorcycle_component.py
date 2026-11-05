from datetime import date, datetime, timezone

from app.extensions import db


class ComponentCategory:
    """Категории компонентов. Совпадают с category в maintenance_presets там, где пересекаются."""

    FLUID = "fluid"
    FILTER = "filter"
    IGNITION = "ignition"
    BRAKE = "brake"
    DRIVE = "drive"
    OTHER = "other"


class ConditionRating:
    """Субъективная оценка владельца. Не расчёт."""

    GOOD = "good"
    OK = "ok"
    BAD = "bad"
    UNKNOWN = "unknown"

    ALL = (GOOD, OK, BAD, UNKNOWN)


class MotorcycleComponent(db.Model):
    """
    Компонент/расходник на конкретном мотоцикле.

    - template_key: ключ из базового набора (component_presets), NULL для ручных.
    - is_active: soft-delete. История работ сохраняется.
    - condition_rating: субъективная оценка владельца, не автодиагностика.
    """

    __tablename__ = "motorcycle_components"

    id = db.Column(db.Integer, primary_key=True)
    motorcycle_id = db.Column(
        db.Integer,
        db.ForeignKey("motorcycles.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    template_key = db.Column(db.String(40), nullable=True)
    name = db.Column(db.String(80), nullable=False)
    category = db.Column(db.String(32), nullable=False, default=ComponentCategory.OTHER)

    manufacturer = db.Column(db.String(80), nullable=True)
    part_number = db.Column(db.String(80), nullable=True)

    interval_km = db.Column(db.Integer, nullable=True)
    interval_days = db.Column(db.Integer, nullable=True)

    last_service_date = db.Column(db.Date, nullable=True)
    last_service_mileage = db.Column(db.Integer, nullable=True)

    condition_rating = db.Column(db.String(16), nullable=True)
    condition_note = db.Column(db.String(256), nullable=True)

    is_active = db.Column(db.Boolean, nullable=False, default=True, index=True)

    created_at = db.Column(
        db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
    )
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    motorcycle = db.relationship("Motorcycle", backref="components")

    __table_args__ = (
        db.UniqueConstraint(
            "motorcycle_id", "template_key", name="uq_component_moto_template"
        ),
        db.Index("idx_component_moto_active", "motorcycle_id", "is_active"),
    )

    def __repr__(self):
        return (
            f"<MotorcycleComponent {self.id} {self.name!r} moto={self.motorcycle_id}>"
        )
