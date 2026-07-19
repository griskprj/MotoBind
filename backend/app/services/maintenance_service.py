from datetime import datetime
from typing import Optional, Dict, Any
from app.models.maintenance import Maintenance, PlannedMaintenance
from app.models.motorcycle import Motorcycle
from app.extensions import db
from app.exceptions import NotFoundError, ForbiddenError, ValidationError


class MaintenanceService:
    """ Сервис для работы с обслуживанием """

    @staticmethod
    def create_maintenance(
        author_id: int,
        moto_id: int,
        category: str,
        title: str,
        description: Optional[str] = None,
        mileage: Optional[int] = None,
        cost: Optional[int] = None,
        date: Optional[datetime] = None
    ) -> Maintenance:
        """ Создает запись о выполненном обслуживании """
        moto = Motorcycle.query.get(moto_id)
        if not moto:
            raise NotFoundError("Мотоцикл не найден")
        
        if moto.owner_id != author_id:
            raise ForbiddenError("Вы можете добавлять обслуживание только для своего мотоцикла")
        
        maintenance = Maintenance(
            author_id=author_id,
            moto_id=moto_id,
            category=category,
            title=title,
            description=description,
            mileage=mileage,
            cost=cost or 0,
            date=date or datetime.now()
        )
        
        db.session.add(maintenance)
        db.session.commit()

    @staticmethod
    def create_planned_maintenance(
        author_id: int,
        moto_id: int,
        category: str,
        title: str,
        description: Optional[str] = None,
        planned_mileage: Optional[int] = None,
    ) -> PlannedMaintenance:
        """ Создает запись планового обслуживания """
        moto = Motorcycle.query.get(moto_id)
        if not moto:
            raise NotFoundError("Мотоцикл не найден")
        
        if moto.owner_id != author_id:
            raise ForbiddenError("Вы можете планировать обслуживание только для своего мотоцикла")
        
        if planned_mileage and planned_mileage < moto.mileage:
            raise ValidationError("Указан пробег меньше пробега мотоцикла")
        
        planned = PlannedMaintenance(
            author_id=author_id,
            moto_id=moto_id,
            title=title,
            category=category,
            description=description,
            planned_mileage=planned_mileage
        )

        db.session.add(planned)
        db.session.commit()

        return planned
    
    @staticmethod
    def mark_planned_as_done(
        planned_id: int,
        author_id: int,
        mileage: int,
        date: datetime,
        cost: Optional[int] = None,
        repeat: bool = False,
        interval: Optional[int] = None,
    ) -> Dict[str, Any]:
        """ Отмечает плановое обслуживание как выполненное """
        planned = PlannedMaintenance.query.get(planned_id)
        if not planned:
            raise NotFoundError("Обслуживание не найдено")
        
        if planned.author_id != author_id:
            raise ForbiddenError("Вы можете отмечать только свое обслуживание")
        
        moto = Motorcycle.query.get(planned.moto_id)
        if not moto:
            raise NotFoundError("Мотоцикл не найден")
        
        maintenance = Maintenance(
            moto_id=moto.id,
            author_id=author_id,
            title=planned.title,
            category=planned.category,
            cost=cost or 0,
            description=planned.description,
            mileage=mileage,
            date=date
        )
        db.session.add(maintenance)

        if mileage > moto.mileage:
            moto.mileage = mileage

        new_planned = None
        if repeat and interval:
            new_planned = PlannedMaintenance(
                author_id=author_id,
                moto_id=moto.id,
                category=planned.category,
                title=planned.title,
                description=planned.description,
                planned_mileage=moto.mileage + interval
            )
            db.session.add(new_planned)

        db.session.delete(planned)
        db.session.commit()

        return {
            'maintenance': maintenance,
            'new_planned': new_planned
        }