from datetime import datetime, timezone

from app.extensions import db


class WorkKind:
    """Виды работ внутри события."""

    REPLACE = "replace"
    INSPECT = "inspect"
    ADJUST = "adjust"
    REPAIR = "repair"
    OTHER = "other"

    ALL = (REPLACE, INSPECT, ADJUST, REPAIR, OTHER)


class MaintenanceEvent(db.Model):
    """
    Событие обслуживания: один визит в сервис / одна сессия.
    """

    __tablename__ = "maintenance_events"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    motorcycle_id = db.Column(
        db.Integer,
        db.ForeignKey("motorcycles.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    date = db.Column(db.Date, nullable=False)
    mileage = db.Column(db.Integer, nullable=True)
    total_cost = db.Column(db.Integer, nullable=False, default=0)
    comment = db.Column(db.Text, nullable=True)

    created_at = db.Column(
        db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
    )
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    works = db.relationship(
        "MaintenanceWork",
        back_populates="event",
        cascade="all, delete-orphan",
        passive_deletes=True,
        order_by="MaintenanceWork.id",
    )

    __table_args__ = (db.Index("idx_event_moto_date", "motorcycle_id", "date"),)

    def __repr__(self):
        return f"<MaintenanceEvent {self.id} moto={self.motorcycle_id} {self.date}>"


class MaintenanceWork(db.Model):
    """
    Работа внутри события. component_id опционален (свободная работа).

    kind='replace' обновляет last_service_* компонента (в сервисе).
    Остальные виды — только история.
    """

    __tablename__ = "maintenance_works"

    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(
        db.Integer,
        db.ForeignKey("maintenance_events.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    component_id = db.Column(
        db.Integer,
        db.ForeignKey("motorcycle_components.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    kind = db.Column(db.String(16), nullable=False, default=WorkKind.OTHER)
    title = db.Column(db.String(80), nullable=True)
    cost = db.Column(db.Integer, nullable=False, default=0)
    note = db.Column(db.Text, nullable=True)

    created_at = db.Column(
        db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
    )

    event = db.relationship("MaintenanceEvent", back_populates="works")
    component = db.relationship("MotorcycleComponent")

    def __repr__(self):
        return f"<MaintenanceWork {self.id} kind={self.kind} comp={self.component_id}>"
