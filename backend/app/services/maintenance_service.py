from datetime import datetime, date, timedelta, timezone
from typing import Any, Dict, Optional, List

from app.exceptions import ForbiddenError, NotFoundError, ValidationError
from app.extensions import db
from app.models.maintenance import Maintenance, MaintenanceStatus
from app.models.motorcycle import Motorcycle
from app.services.notification_service import NotificationService
from app.services.motorcycle_service import MotorcycleService
from app.constants.maintenance_presets import (
    get_presets_for_motorcycle,
    calculate_interval,
)


class MaintenanceService:
    """Сервис для работы с обслуживанием"""

    @staticmethod
    def create_maintenance(
        author_id: int,
        moto_id: int,
        category: str,
        title: str,
        description: Optional[str] = None,
        planned_mileage: Optional[int] = None,
        planned_date: Optional[str] = None,
        completed_mileage: Optional[int] = None,
        completed_date: Optional[str] = None,
        cost: Optional[int] = None,
    ) -> Maintenance:
        """Создает запись обслуживания"""
        moto = db.session.get(Motorcycle, moto_id)
        if not moto:
            raise NotFoundError("Мотоцикл не найден")

        if moto.owner_id != author_id:
            raise ForbiddenError("Вы можете добавлять обслуживание только для своего мотоцикла")

        planned_date_obj = None
        if planned_date:
            try:
                planned_date_obj = datetime.strptime(planned_date, "%Y-%m-%d").date()
            except ValueError:
                raise ValidationError("Неверный формат даты. Используйте ГГГГ-ММ-ДД")
        
        completed_date_obj = None
        if completed_date:
            try:
                completed_date_obj = datetime.strptime(completed_date, "%Y-%m-%d").date()
            except ValueError:
                raise ValidationError("Неверный формат даты. Используйте ГГГГ-ММ-ДД")

        if completed_mileage is not None:
            status = MaintenanceStatus.COMPLETED.value
        elif planned_mileage is not None or planned_date_obj is not None:
            status = MaintenanceStatus.PLANNED.value
        else:
            raise ValidationError("Укажите либо плановые, либо выполненные поля")

        maintenance = Maintenance(
            author_id=author_id,
            moto_id=moto_id,
            category=category,
            title=title,
            description=description,
            planned_mileage=planned_mileage,
            planned_date=planned_date_obj,
            completed_mileage=completed_mileage,
            completed_date=completed_date_obj,
            cost=cost or 0,
            status=status,
        )

        db.session.add(maintenance)
        db.session.commit()
        return maintenance

    @staticmethod
    def quick_start(
        user_id: int,
        moto_id: int,
        current_mileage: int,
        drive_type: str = "chain",
        style: str = "normal",
        terrain: str = "mixed",
    ) -> dict:
        """Создает базовый набор плановых ТО для мотоцикла"""
        moto = MotorcycleService.get_motorcycle_by_id(moto_id, user_id)

        if current_mileage is None or current_mileage < 0:
            raise ValidationError("Некорректный пробег")

        existing = Maintenance.query.filter_by(moto_id=moto_id).count()
        if existing > 0:
            raise ValidationError("У мотоцикла уже есть обслуживания")

        MotorcycleService.set_mileage(moto, current_mileage)
        moto.drive_type = drive_type

        presets = get_presets_for_motorcycle(drive_type)
        today = datetime.now(timezone.utc).date()
        created = []

        for preset in presets:
            interval = calculate_interval(preset, style, terrain)

            planned_mileage = current_mileage + interval["interval_km"]
            planned_date = today + timedelta(days=interval["interval_days"])

            record = Maintenance(
                moto_id=moto_id,
                author_id=user_id,
                title=preset["title"],
                description=preset["description"],
                category=preset["category"],
                status=MaintenanceStatus.PLANNED.value,
                planned_mileage=planned_mileage,
                planned_date=planned_date,
            )

            db.session.add(record)
            created.append({
                "title": preset["title"],
                "planned_mileage": planned_mileage,
                "planned_date": planned_date.isoformat(),
                "interval_km": interval["interval_km"],
            })

        db.session.commit()

        NotificationService.send_notification(
            user_id=user_id,
            type="system",
            title="Базовое обслуживание создано",
            content=f"Для {moto.name} создано {len(created)} плановых работ",
            link="/maintenance",
        )

        return {
            "message": f"Создано {len(created)} обслуживания",
            "created": created,
            "moto": moto.to_dict(),
        }

    @staticmethod
    def mark_planned_as_done(
        planned_id: int,
        author_id: int,
        mileage: int,
        completed_date: Optional[str] = None,
        cost: Optional[int] = None,
        repeat: bool = False,
        interval: Optional[int] = None,
        interval_days: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Отмечает плановое обслуживание как выполненное"""
        planned = db.session.get(Maintenance, planned_id)
        if not planned:
            raise NotFoundError("Обслуживание не найдено")

        if planned.author_id != author_id:
            raise ForbiddenError("Вы можете отмечать только свое обслуживание")

        if planned.status == MaintenanceStatus.COMPLETED.value:
            raise ValidationError("Обслуживание уже выполнено")

        completed_date_obj = None
        if completed_date:
            try:
                completed_date_obj = datetime.strptime(completed_date, "%Y-%m-%d").date()
            except ValueError:
                raise ValidationError("Неверный формат даты. Используйте ГГГГ-ММ-ДД")

        moto = MotorcycleService.get_motorcycle_by_id(planned.moto_id, author_id)

        planned.status = MaintenanceStatus.COMPLETED.value
        planned.completed_mileage = mileage
        planned.completed_date = completed_date_obj
        planned.cost = cost or 0

        if mileage > moto.mileage:
            MotorcycleService.set_mileage(moto, mileage)

        new_planned = None
        if repeat:
            new_planned_data = {
                'author_id': author_id,
                'moto_id': moto.id,
                'category': planned.category,
                'title': planned.title,
                'description': planned.description,
                'status': MaintenanceStatus.PLANNED.value,
            }

            if interval:
                new_planned_data['planned_mileage'] = moto.mileage + interval
            elif interval_days:
                today = date.today()
                new_planned_data['planned_date'] = today + timedelta(days=interval_days)
            else:
                raise ValidationError("Укажите интервал (пробег или дни)")

            new_planned = Maintenance(**new_planned_data)
            db.session.add(new_planned)

        db.session.commit()

        return {"maintenance": planned, "new_planned": new_planned}

    @staticmethod
    def update_maintenance(
        maintenance_id: int, user_id: int, **kwargs
    ) -> Maintenance:
        """
        Обновляет данные обслуживания
        """
        maintenance = MaintenanceService.get_maintenance_by_id(
            user_id, maintenance_id
        )

        if "moto_id" in kwargs and kwargs["moto_id"] is not None:
            moto = db.session.get(Motorcycle, kwargs["moto_id"])
            if not moto:
                raise NotFoundError("Мотоцикл не найден")
            if moto.owner_id != user_id:
                raise ForbiddenError("Вы не являетесь владельцем этого мотоцикла")

        if "planned_date" in kwargs and kwargs["planned_date"] is not None:
            try:
                kwargs["planned_date"] = datetime.strptime(kwargs["planned_date"], "%Y-%m-%d").date()
            except ValueError:
                raise ValidationError("Неверный формат даты. Используйте ГГГГ-ММ-ДД")

        if "completed_date" in kwargs and kwargs["completed_date"] is not None:
            try:
                kwargs["completed_date"] = datetime.strptime(kwargs["completed_date"], "%Y-%m-%d").date()
            except ValueError:
                raise ValidationError("Неверный формат даты. Используйте ГГГГ-ММ-ДД")

        for key, value in kwargs.items():
            if hasattr(maintenance, key) and value is not None:
                setattr(maintenance, key, value)

        if "completed_date" in kwargs or "completed_mileage" in kwargs:
            MaintenanceService._recompute_status(maintenance)

        db.session.commit()
        return maintenance

    @staticmethod
    def delete_maintenance(maintenance_id: int, user_id: int) -> None:
        """Удаляет обслуживание"""
        maintenance = MaintenanceService.get_maintenance_by_id(
            user_id, maintenance_id
        )
        db.session.delete(maintenance)
        db.session.commit()

    @staticmethod
    def get_maintenance_by_id(user_id: int, maintenance_id: int) -> Maintenance:
        """Получить обслуживание по ID"""
        maintenance = db.session.get(Maintenance, maintenance_id)
        if not maintenance:
            raise NotFoundError("Обслуживание не найдено")

        if int(maintenance.author_id) != int(user_id):
            raise ForbiddenError("Вы не являетесь автором этого обслуживания")

        return maintenance

    @staticmethod
    def get_maintenances_by_motorcycle(user_id: int, moto_id: int) -> List[Maintenance]:
        """Получает обслуживания мотоцикла"""
        moto = MotorcycleService.get_motorcycle_by_id(moto_id, user_id)
        return moto.maintenances or []

    @staticmethod
    def _recompute_status(record: Maintenance) -> None:
        """
        Пересчитывает статус по наличию completed/planned полей
        Called after update to keep status consistent with filled fields
        """
        if record.completed_mileage is not None or record.completed_date is not None:
            record.status = MaintenanceStatus.COMPLETED.value
        elif record.planned_mileage is not None or record.planned_date is not None:
            record.status = MaintenanceStatus.PLANNED.value