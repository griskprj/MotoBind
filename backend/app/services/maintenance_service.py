from enum import Enum
from datetime import datetime, date
from typing import Any, Dict, Optional, List

from app.exceptions import ForbiddenError, NotFoundError, ValidationError
from app.extensions import db
from app.models.maintenance import Maintenance
from app.models.motorcycle import Motorcycle
from app.services.motorcycle_service import MotorcycleService


class MaintenanceStatus (Enum):
    COMPLETED = "completed"
    PLANNED = "planned"
    SOON = "soon"
    OVERDUE = "overdue"

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
        moto = Motorcycle.query.get(moto_id)
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

        if completed_mileage is not None and completed_date_obj is not None:
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
    def mark_planned_as_done(
        planned_id: int,
        author_id: int,
        mileage: int,
        date: str,
        cost: Optional[int] = None,
        repeat: bool = False,
        interval: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Отмечает плановое обслуживание как выполненное"""
        planned = Maintenance.query.get(planned_id)
        if not planned:
            raise NotFoundError("Обслуживание не найдено")

        if planned.author_id != author_id:
            raise ForbiddenError("Вы можете отмечать только свое обслуживание")

        if planned.status == 'completed':
            raise ValidationError("Обслуживание уже выполнено")
        
        # Преобразуем дату
        completed_date_obj = None
        if date:
            try:
                completed_date_obj = datetime.strptime(date, "%Y-%m-%d").date()
            except ValueError:
                raise ValidationError("Неверный формат даты. Используйте ГГГГ-ММ-ДД")

        moto = MotorcycleService.get_motorcycle_by_id(planned.moto_id, author_id)

        planned.status = 'completed'
        planned.completed_mileage = mileage
        planned.completed_date = completed_date_obj
        planned.cost = cost or 0

        if mileage > moto.mileage:
            moto.mileage = mileage

        new_planned = None
        if repeat and interval:
            new_planned = Maintenance(
                author_id=author_id,
                moto_id=moto.id,
                category=planned.category,
                title=planned.title,
                description=planned.description,
                planned_mileage=moto.mileage + interval,
                status='planned',
            )
            db.session.add(new_planned)

        db.session.commit()

        return {"maintenance": planned, "new_planned": new_planned}

    @staticmethod
    def update_maintenance(
        maintenance_id: int, user_id: int, **kwargs
    ) -> Maintenance:
        """Обновляет данные обслуживания"""
        maintenance = MaintenanceService.get_maintenance_by_id(
            user_id, maintenance_id
        )

        if "moto_id" in kwargs and kwargs["moto_id"] is not None:
            moto = Motorcycle.query.get(kwargs["moto_id"])
            if not moto:
                raise NotFoundError("Мотоцикл не найден")
            if moto.owner_id != user_id:
                raise ForbiddenError("Вы не являетесь владельцем этого мотоцикла")

        if "planned_mileage" in kwargs and kwargs["planned_mileage"] is not None:
            current_moto_id = kwargs.get("moto_id", maintenance.moto_id)
            moto = Motorcycle.query.get(current_moto_id)
            if moto and kwargs["planned_mileage"] < moto.mileage:
                raise ValidationError("Указан пробег меньше пробега мотоцикла")

        for key, value in kwargs.items():
            if hasattr(maintenance, key) and value is not None:
                setattr(maintenance, key, value)

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
        maintenance = Maintenance.query.get(maintenance_id)
        if not maintenance:
            raise NotFoundError("Обслуживание не найдено")

        if int(maintenance.author_id) != int(user_id):
            raise ForbiddenError("Вы не являетесь автором этого обслуживания")

        return maintenance

    @staticmethod
    def get_last_maintenance_by_category(user_id: int, category: str) -> Maintenance:
        """Получить обслуживание по категории"""
        maintenances = Maintenance.query.filter(
            category=category, author_id=user_id
        ).all()
        last_maintenance = None
        for m in maintenances:
            if m.mileage and m.mileage > last_maintenance.mileage:
                last_maintenance = m

        return m.to_dict()

    @staticmethod
    def get_maintenances_by_motorcycle(user_id: int, moto_id: int) -> List[Maintenance]:
        """Получает обслуживания мотоцикла"""
        moto = MotorcycleService.get_motorcycle_by_id(moto_id)
        return [m for m in moto.maintenances]