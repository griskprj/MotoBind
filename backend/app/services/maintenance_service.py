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

        return maintenance

    @staticmethod
    def create_planned_maintenance(
        author_id: int,
        moto_id: int,
        category: str,
        title: str,
        planned_mileage: int,
        description: Optional[str] = None,
    ) -> PlannedMaintenance:
        """ Создает запись планового обслуживания """
        moto = Motorcycle.query.get(moto_id)
        if not moto:
            raise NotFoundError("Мотоцикл не найден")
        
        if moto.owner_id != author_id:
            raise ForbiddenError("Вы можете планировать обслуживание только для своего мотоцикла")
        
        if planned_mileage and planned_mileage < moto.mileage:
            raise ValidationError("Указан пробег меньше пробега мотоцикла")
        
        print(planned_mileage)
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
    
    @staticmethod
    def update_planned_maintenance(maintenance_id: int, user_id: int, **kwargs) -> PlannedMaintenance:
        """ Обновляет данные запланированного обслуживания """
        plan_maintenance = MaintenanceService.get_planned_maintenance_by_id(user_id, maintenance_id)
        
        if 'moto_id' in kwargs and kwargs['moto_id'] is not None:
            moto = Motorcycle.query.get(kwargs['moto_id'])
            if not moto:
                raise NotFoundError("Мотоцикл не найден")
            if moto.owner_id != user_id:
                raise ForbiddenError("Вы не являетесь владельцем этого мотоцикла")

        if 'planned_mileage' in kwargs and kwargs['planned_mileage'] is not None:
            current_moto_id = kwargs.get('moto_id', plan_maintenance.moto_id)
            moto = Motorcycle.query.get(current_moto_id)
            if moto and kwargs['planned_mileage'] < moto.mileage:
                raise ValidationError("Указан пробег меньше пробега мотоцикла")

        for key, value in kwargs.items():
            if hasattr(plan_maintenance, key) and value is not None:
                setattr(plan_maintenance, key, value)

        db.session.commit()
        return plan_maintenance
    
    @staticmethod
    def delete_plan_maintenance(maintenance_id: int, user_id: int) -> None:
        """ Удаляет плановое обслуживание """
        plan_maintenance = MaintenanceService.get_maintenance_by_id(user_id, maintenance_id)
        db.session.delete(plan_maintenance)
        db.session.commit()

    @staticmethod
    def get_maintenance_by_id(user_id: int, maintenance_id: int) -> Maintenance:
        """ Получить обслуживание по ID """
        maintenance = Maintenance.query.get(maintenance_id)
        if not maintenance:
            raise NotFoundError("Обслуживание не найдено")
        
        if int(maintenance.author_id) != int(user_id):
            raise ForbiddenError("Вы не являетесь автором этого обслуживания")
        
        return maintenance
        
    @staticmethod
    def get_planned_maintenance_by_id(user_id: int, maintenance_id: int) -> Maintenance:
        """ Получить плановое обслуживание по ID """
        planned_maintenance = PlannedMaintenance.query.get(maintenance_id)
        if not planned_maintenance:
            raise NotFoundError("Обслуживание не найдено")
        
        if planned_maintenance.author_id != user_id:
            raise ForbiddenError("Вы не являетесь автором этого обслуживания")
        
        return planned_maintenance