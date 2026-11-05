from datetime import date, datetime, timedelta, timezone
from typing import Optional

from app.exceptions import ForbiddenError, NotFoundError, ValidationError
from app.extensions import db
from app.models.maintenance_event import MaintenanceEvent, MaintenanceWork, WorkKind
from app.models.motorcycle import Motorcycle
from app.models.motorcycle_component import MotorcycleComponent
from app.utils.helpers import get_motorcycle_or_404


class EventService:
    """Сервис событий обслуживания."""

    # ============================================================
    # ЧТЕНИЕ
    # ============================================================

    @staticmethod
    def list_for_motorcycle(
        user_id: int, moto_id: int, page: int = 1, per_page: int = 20
    ) -> dict:
        get_motorcycle_or_404(moto_id, user_id)
        page = max(1, page)
        per_page = max(1, min(per_page, 100))

        query = MaintenanceEvent.query.filter_by(motorcycle_id=moto_id).order_by(
            MaintenanceEvent.date.desc(), MaintenanceEvent.id.desc()
        )
        total = query.count()
        items = query.offset((page - 1) * per_page).limit(per_page).all()
        pages = (total + per_page - 1) // per_page if total else 0

        return {
            "events": items,
            "total": total,
            "page": page,
            "per_page": per_page,
            "pages": pages,
        }

    @staticmethod
    def get_by_id(user_id: int, moto_id: int, event_id: int) -> MaintenanceEvent:
        get_motorcycle_or_404(moto_id, user_id)
        event = db.session.get(MaintenanceEvent, event_id)
        if not event or event.motorcycle_id != moto_id:
            raise NotFoundError("Событие не найдено")
        return event

    # ============================================================
    # СОЗДАНИЕ
    # ============================================================

    @staticmethod
    def create(
        user_id: int,
        moto_id: int,
        date_str: str,
        mileage: Optional[int],
        total_cost: Optional[int],
        comment: Optional[str],
        works: list[dict],
    ) -> MaintenanceEvent:
        moto = get_motorcycle_or_404(moto_id, user_id)
        event_date = EventService._parse_date(date_str)

        if not works:
            raise ValidationError("Нужна хотя бы одна работа")

        components = EventService._resolve_components(moto_id, works)

        event = MaintenanceEvent(
            user_id=user_id,
            motorcycle_id=moto_id,
            date=event_date,
            mileage=mileage,
            comment=comment,
            total_cost=0,
        )
        db.session.add(event)
        db.session.flush()

        for w in works:
            comp = components.get(w.get("component_id"))
            work = MaintenanceWork(
                event_id=event.id,
                component_id=comp.id if comp else None,
                kind=w.get("kind") or WorkKind.OTHER,
                title=(w.get("title") or (comp.name if comp else None)),
                cost=w.get("cost") or 0,
                note=w.get("note"),
            )
            db.session.add(work)

        explicit_total = total_cost
        if explicit_total is None:
            event.total_cost = sum((w.get("cost") or 0) for w in works)
        else:
            event.total_cost = explicit_total

        EventService._apply_last_service(event, works, components)

        if mileage is not None and (moto.mileage or 0) < mileage:
            from app.services.motorcycle_service import MotorcycleService

            MotorcycleService.set_mileage(moto, mileage)

        db.session.commit()
        return event

    # ============================================================
    # ОБНОВЛЕНИЕ
    # ============================================================

    @staticmethod
    def update(
        user_id: int, moto_id: int, event_id: int, **updates
    ) -> MaintenanceEvent:
        event = EventService.get_by_id(user_id, moto_id, event_id)

        if "date" in updates and updates["date"]:
            event.date = EventService._parse_date(updates["date"])

        if "mileage" in updates:
            event.mileage = updates["mileage"]

        if "comment" in updates:
            event.comment = updates["comment"]

        if "works" in updates and updates["works"] is not None:
            new_works = updates["works"]
            components = EventService._resolve_components(moto_id, new_works)

            for w in list(event.works):
                db.session.delete(w)
            db.session.flush()

            for w in new_works:
                comp = components.get(w.get("component_id"))
                work = MaintenanceWork(
                    event_id=event.id,
                    component_id=comp.id if comp else None,
                    kind=w.get("kind") or WorkKind.OTHER,
                    title=(w.get("title") or (comp.name if comp else None)),
                    cost=w.get("cost") or 0,
                    note=w.get("note"),
                )
                db.session.add(work)

            EventService._recalc_components_last_service(event)

        if "total_cost" in updates and updates["total_cost"] is not None:
            event.total_cost = updates["total_cost"]

        event.updated_at = datetime.now(timezone.utc)
        db.session.commit()
        return event

    # ============================================================
    # УДАЛЕНИЕ
    # ============================================================

    @staticmethod
    def delete(user_id: int, moto_id: int, event_id: int) -> None:
        event = EventService.get_by_id(user_id, moto_id, event_id)

        affected_component_ids = {
            w.component_id for w in event.works if w.component_id is not None
        }

        db.session.delete(event)
        db.session.flush()

        EventService._recalc_components_by_ids(affected_component_ids)

        db.session.commit()

    # ============================================================
    # ХЕЛПЕРЫ
    # ============================================================

    @staticmethod
    def _parse_date(value: str) -> date:
        try:
            return datetime.strptime(value, "%Y-%m-%d").date()
        except (ValueError, TypeError):
            raise ValidationError("Неверный формат даты. Используйте ГГГГ-ММ-ДД")

    @staticmethod
    def _resolve_components(
        moto_id: int, works: list[dict]
    ) -> dict[int, MotorcycleComponent]:
        """Загружает компоненты по id, проверяет принадлежность мотоциклу."""
        ids = {w.get("component_id") for w in works if w.get("component_id")}
        if not ids:
            return {}

        components = MotorcycleComponent.query.filter(
            MotorcycleComponent.id.in_(ids),
            MotorcycleComponent.motorcycle_id == moto_id,
        ).all()
        found = {c.id: c for c in components}

        missing = ids - set(found.keys())
        if missing:
            raise ValidationError(
                f"Компоненты не найдены на этом мотоцикле: {sorted(missing)}"
            )
        return found

    @staticmethod
    def _apply_last_service(
        event: MaintenanceEvent, works: list[dict], components: dict
    ) -> None:
        """Для kind='replace' обновляет last_service_* компонента."""
        for w in works:
            if (w.get("kind") or WorkKind.OTHER) != WorkKind.REPLACE:
                continue
            cid = w.get("component_id")
            comp = components.get(cid) if cid else None
            if comp is None:
                continue
            if event.date is not None:
                comp.last_service_date = event.date
            if event.mileage is not None:
                comp.last_service_mileage = event.mileage

    @staticmethod
    def _recalc_components_last_service(event: MaintenanceEvent) -> None:
        """Пересчитать last_service_* для компонентов, затронутых работами event."""
        ids = {w.component_id for w in event.works if w.component_id is not None}
        EventService._recalc_components_by_ids(ids)

    @staticmethod
    def _recalc_components_by_ids(component_ids: set[int]) -> None:
        """
        Для каждого компонента берём последнюю replace-работу (по дате события,
        затем по id) и выставляем last_service_date/mileage.
        Если replace-работ больше нет — обнуляем last_service_*.
        """
        if not component_ids:
            return

        for cid in component_ids:
            comp = db.session.get(MotorcycleComponent, cid)
            if comp is None:
                continue

            latest = (
                MaintenanceWork.query.join(
                    MaintenanceEvent, MaintenanceEvent.id == MaintenanceWork.event_id
                )
                .filter(
                    MaintenanceWork.component_id == cid,
                    MaintenanceWork.kind == WorkKind.REPLACE,
                )
                .order_by(MaintenanceEvent.date.desc(), MaintenanceWork.id.desc())
                .first()
            )
            if latest is None:
                comp.last_service_date = None
                comp.last_service_mileage = None
            else:
                comp.last_service_date = latest.event.date
                comp.last_service_mileage = latest.event.mileage
