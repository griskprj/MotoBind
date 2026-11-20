from datetime import datetime, timezone
from typing import Optional

from app.constants.component_presets import build_component_set
from app.exceptions import ConflictError, ForbiddenError, NotFoundError, ValidationError
from app.extensions import db
from app.models.maintenance_event import MaintenanceWork, WorkKind
from app.models.motorcycle import Motorcycle
from app.models.motorcycle_component import (
    ComponentCategory,
    ConditionRating,
    MotorcycleComponent,
)
from app.utils.helpers import get_motorcycle_or_404


class ComponentService:
    """Сервис компонентов мотоцикла."""

    # ============================================================
    # ЧТЕНИЕ
    # ============================================================

    @staticmethod
    def list_for_motorcycle(
        user_id: int, moto_id: int, include_inactive: bool = False
    ) -> list[MotorcycleComponent]:
        get_motorcycle_or_404(moto_id, user_id)

        query = MotorcycleComponent.query.filter_by(motorcycle_id=moto_id)
        if not include_inactive:
            query = query.filter_by(is_active=True)
        return query.order_by(
            MotorcycleComponent.is_active.desc(),
            MotorcycleComponent.category.asc(),
            MotorcycleComponent.name.asc(),
        ).all()

    @staticmethod
    def get_by_id(
        user_id: int, moto_id: int, component_id: int, include_inactive: bool = False
    ) -> MotorcycleComponent:
        get_motorcycle_or_404(moto_id, user_id)
        component = db.session.get(MotorcycleComponent, component_id)
        if not component or component.motorcycle_id != moto_id:
            raise NotFoundError("Компонент не найден")
        if not include_inactive and not component.is_active:
            raise NotFoundError("Компонент не найден")
        return component

    # ============================================================
    # СОЗДАНИЕ / ОБНОВЛЕНИЕ
    # ============================================================

    @staticmethod
    def create(user_id: int, moto_id: int, **kwargs) -> MotorcycleComponent:
        get_motorcycle_or_404(moto_id, user_id)

        name = (kwargs.get("name") or "").strip()
        if not name:
            raise ValidationError("Название компонента обязательно")

        category = kwargs.get("category") or ComponentCategory.OTHER
        if category not in (
            ComponentCategory.FLUID,
            ComponentCategory.FILTER,
            ComponentCategory.IGNITION,
            ComponentCategory.BRAKE,
            ComponentCategory.DRIVE,
            ComponentCategory.OTHER,
        ):
            raise ValidationError("Недопустимая категория")

        interval_km = kwargs.get("interval_km")
        interval_days = kwargs.get("interval_days")
        ComponentService._validate_intervals(interval_km, interval_days)

        component = MotorcycleComponent(
            motorcycle_id=moto_id,
            template_key=None,
            name=name,
            category=category,
            manufacturer=kwargs.get("manufacturer") or None,
            part_number=kwargs.get("part_number") or None,
            interval_km=interval_km,
            interval_days=interval_days,
            last_service_date=kwargs.get("last_service_date"),
            last_service_mileage=kwargs.get("last_service_mileage"),
            condition_rating=ComponentService._validate_condition(
                kwargs.get("condition_rating")
            ),
            condition_note=(kwargs.get("condition_note") or None),
            is_active=True,
        )
        db.session.add(component)
        db.session.commit()
        return component

    @staticmethod
    def update(
        user_id: int, moto_id: int, component_id: int, **updates
    ) -> MotorcycleComponent:
        component = ComponentService.get_by_id(user_id, moto_id, component_id)

        if "name" in updates:
            name = (updates["name"] or "").strip()
            if not name:
                raise ValidationError("Название компонента обязательно")
            component.name = name

        if "category" in updates and updates["category"] is not None:
            component.category = updates["category"]

        for field in ("manufacturer", "part_number", "condition_note"):
            if field in updates:
                setattr(component, field, updates[field] or None)

        if "interval_km" in updates or "interval_days" in updates:
            new_km = updates.get("interval_km", component.interval_km)
            new_days = updates.get("interval_days", component.interval_days)
            ComponentService._validate_intervals(new_km, new_days)
            component.interval_km = new_km
            component.interval_days = new_days

        if "last_service_date" in updates:
            component.last_service_date = updates["last_service_date"]
        if "last_service_mileage" in updates:
            component.last_service_mileage = updates["last_service_mileage"]

        if "condition_rating" in updates:
            component.condition_rating = ComponentService._validate_condition(
                updates["condition_rating"]
            )

        component.updated_at = datetime.now(timezone.utc)
        db.session.commit()
        return component

    @staticmethod
    def deactivate(user_id: int, moto_id: int, component_id: int) -> None:
        """Soft-delete. История работ сохраняется."""
        component = ComponentService.get_by_id(user_id, moto_id, component_id)
        component.is_active = False
        component.updated_at = datetime.now(timezone.utc)
        db.session.commit()

    @staticmethod
    def reactivate(
        user_id: int, moto_id: int, component_id: int
    ) -> MotorcycleComponent:
        """Вернуть компонент в активные (если был soft-deleted)."""
        component = ComponentService.get_by_id(
            user_id, moto_id, component_id, include_inactive=True
        )
        component.is_active = True
        component.updated_at = datetime.now(timezone.utc)
        db.session.commit()
        return component

    # ============================================================
    # БАЗОВЫЙ НАБОР
    # ============================================================

    @staticmethod
    def apply_template(
        user_id: int,
        moto_id: int,
        style: str = "normal",
        terrain: str = "mixed",
    ) -> dict:
        """
        Создаёт базовый набор компонентов. Идемпотентно:
        - существующие template_key (даже soft-deleted) пропускаются;
        - возвращает {created: [...], skipped: [...]}.
        """
        moto = get_motorcycle_or_404(moto_id, user_id)

        drive_type = moto.drive_type or "chain"
        if drive_type not in ("chain", "belt", "shaft"):
            drive_type = "chain"

        presets = build_component_set(
            drive_type=drive_type, style=style, terrain=terrain
        )

        existing_keys = {
            row.template_key
            for row in MotorcycleComponent.query.filter_by(motorcycle_id=moto_id).all()
            if row.template_key
        }

        created: list[dict] = []
        skipped: list[dict] = []

        for p in presets:
            key = p["template_key"]
            if key in existing_keys:
                skipped.append({"template_key": key, "name": p["name"]})
                continue

            component = MotorcycleComponent(
                motorcycle_id=moto_id,
                template_key=key,
                name=p["name"],
                category=p["category"],
                interval_km=p["interval_km"],
                interval_days=p["interval_days"],
                is_active=True,
            )
            db.session.add(component)
            created.append({"template_key": key, "name": p["name"]})

        db.session.commit()

        return {
            "created": created,
            "skipped": skipped,
            "drive_type": drive_type,
            "counts": {"created": len(created), "skipped": len(skipped)},
        }

    # ============================================================
    # ИСТОРИЯ
    # ============================================================

    @staticmethod
    def get_history(
        user_id: int, moto_id: int, component_id: int
    ) -> list[MaintenanceWork]:
        """Работы по компоненту (из MaintenanceWork)."""
        ComponentService.get_by_id(
            user_id, moto_id, component_id, include_inactive=True
        )
        return (
            MaintenanceWork.query.filter_by(component_id=component_id)
            .order_by(MaintenanceWork.created_at.desc())
            .all()
        )

    # ============================================================
    # ХЕЛПЕРЫ
    # ============================================================

    @staticmethod
    def _validate_intervals(interval_km: Optional[int], interval_days: Optional[int]):
        """
        0 разрешён и трактуется как «ограничение не задано»
        (см. расчёт ресурса в HealthService). Отрицательные — ошибка.
        """
        if interval_km is not None and interval_km < 0:
            raise ValidationError("Интервал по пробегу не может быть отрицательным")
        if interval_days is not None and interval_days < 0:
            raise ValidationError("Интервал по времени не может быть отрицательным")

    @staticmethod
    def _validate_condition(value: Optional[str]) -> Optional[str]:
        if value is None:
            return None
        if value not in ConditionRating.ALL:
            raise ValidationError("Недопустимая оценка состояния")
        return value
