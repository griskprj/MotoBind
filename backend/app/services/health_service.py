from datetime import date, datetime, timezone
from typing import Optional

from app.extensions import db
from app.models.motorcycle import Motorcycle
from app.models.motorcycle_component import (
    ComponentCategory,
    ConditionRating,
    MotorcycleComponent,
)
from app.services.reminder_service import (
    MAINTENANCE_SOON_THRESHOLD_DAYS,
    MAINTENANCE_SOON_THRESHOLD_KM,
)
from app.utils.helpers import get_motorcycle_or_404


class ComponentStatus:
    OK = "ok"
    DUE_SOON = "due_soon"
    OVERDUE = "overdue"
    UNKNOWN = "unknown"


class HealthService:
    """Расчёт ресурса/состояния компонентов и сводки по мотоциклу."""

    # ============================================================
    # РЕСУРС КОМПОНЕНТА
    # ============================================================

    @staticmethod
    def calculate_component_resource(
        component: MotorcycleComponent,
        current_mileage: Optional[int],
        today: Optional[date] = None,
    ) -> dict:
        """
        Возвращает ориентировочный остаток ресурса.

        Правила:
        - interval_km=0 / interval_days=0 трактуем как «не задано».
        - Если заданы оба ограничения — берём то, что наступит раньше.
        - Нет данных (нет интервала / нет last_service_*) → status=unknown.
        """
        today = today or date.today()

        interval_km = component.interval_km or None
        interval_days = component.interval_days or None

        remaining_km: Optional[int] = None
        remaining_days: Optional[int] = None

        if (
            interval_km
            and current_mileage is not None
            and component.last_service_mileage is not None
        ):
            remaining_km = interval_km - (
                current_mileage - component.last_service_mileage
            )

        if interval_days and component.last_service_date is not None:
            last_date = component.last_service_date
            if isinstance(last_date, datetime):
                last_date = last_date.date()
            remaining_days = interval_days - (today - last_date).days

        candidates = [v for v in (remaining_km, remaining_days) if v is not None]
        if not candidates:
            return {
                "status": ComponentStatus.UNKNOWN,
                "remaining_km": None,
                "remaining_days": None,
                "limited_by": None,
                "is_estimate": True,
            }

        remaining = min(candidates)
        limited_by = "km" if remaining == remaining_km else "days"

        if remaining <= 0:
            status = ComponentStatus.OVERDUE
        elif (
            remaining_km is not None and remaining_km <= MAINTENANCE_SOON_THRESHOLD_KM
        ) or (
            remaining_days is not None
            and remaining_days <= MAINTENANCE_SOON_THRESHOLD_DAYS
        ):
            status = ComponentStatus.DUE_SOON
        else:
            status = ComponentStatus.OK

        return {
            "status": status,
            "remaining_km": remaining_km,
            "remaining_days": remaining_days,
            "limited_by": limited_by,
            "is_estimate": True,
        }

    # ============================================================
    # СВОДКА ПО МОТОЦИКЛУ
    # ============================================================

    @staticmethod
    def get_motorcycle_health(user_id: int, moto_id: int) -> dict:
        moto = get_motorcycle_or_404(moto_id, user_id)
        components = (
            MotorcycleComponent.query.filter_by(motorcycle_id=moto_id, is_active=True)
            .order_by(
                MotorcycleComponent.category.asc(),
                MotorcycleComponent.name.asc(),
            )
            .all()
        )

        current_mileage = moto.mileage
        today = date.today()

        items: list[dict] = []
        for c in components:
            resource = HealthService.calculate_component_resource(
                c, current_mileage, today
            )
            items.append(
                {
                    "id": c.id,
                    "name": c.name,
                    "category": c.category,
                    "template_key": c.template_key,
                    "condition_rating": c.condition_rating,
                    "is_safety": c.category == ComponentCategory.BRAKE,
                    **resource,
                }
            )

        overdue = [i for i in items if i["status"] == ComponentStatus.OVERDUE]
        due_soon = [i for i in items if i["status"] == ComponentStatus.DUE_SOON]
        unknown = [i for i in items if i["status"] == ComponentStatus.UNKNOWN]
        ok = [i for i in items if i["status"] == ComponentStatus.OK]

        bad_by_owner = [
            i for i in items if i.get("condition_rating") == ConditionRating.BAD
        ]

        safety_attention = [
            i
            for i in items
            if i["is_safety"]
            and (
                i["status"] == ComponentStatus.OVERDUE
                or i.get("condition_rating") == ConditionRating.BAD
            )
        ]
        safety_ids = {i["id"] for i in safety_attention}

        attention: list[dict] = []
        seen = set()
        for src in (overdue, due_soon, bad_by_owner):
            for i in src:
                if i["id"] in safety_ids or i["id"] in seen:
                    continue
                seen.add(i["id"])
                attention.append(i)

        assessed = [
            i
            for i in items
            if i["id"] not in safety_ids and i["status"] != ComponentStatus.UNKNOWN
        ]
        overall = None
        overall_label = "недостаточно данных"
        if assessed:
            ok_count = sum(1 for i in assessed if i["status"] == ComponentStatus.OK)
            overall = round(ok_count / len(assessed) * 100)
            if overall >= 80:
                overall_label = "хорошее"
            elif overall >= 50:
                overall_label = "удовлетворительное"
            else:
                overall_label = "требует внимания"

        upcoming = sorted(
            due_soon + overdue,
            key=lambda i: (
                i["remaining_km"] if i["remaining_km"] is not None else 10**9,
                i["remaining_days"] if i["remaining_days"] is not None else 10**9,
            ),
        )

        return {
            "motorcycle_id": moto_id,
            "current_mileage": current_mileage,
            "is_estimate": True,
            "overall": {
                "percent": overall,
                "label": overall_label,
                "is_estimate": True,
            },
            "counts": {
                "total": len(items),
                "ok": len(ok),
                "due_soon": len(due_soon),
                "overdue": len(overdue),
                "unknown": len(unknown),
                "safety_attention": len(safety_attention),
            },
            "safety_attention": safety_attention,
            "attention": attention,
            "upcoming": upcoming,
            "no_data": unknown,
            "items": items,
        }
