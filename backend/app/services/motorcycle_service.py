from typing import Optional, List
from app.models.motorcycle import Motorcycle
from app.models.maintenance_node import MaintenanceNode
from app.extensions import db
from app.exceptions import NotFoundError, ForbiddenError, ValidationError


class MotorcycleService:
    """ Сервис для работы с мотоциклами """

    DEFAULT_NODES = [
        {'title': 'Двигатель', 'category': 'engine'},
        {'title': 'Привод', 'category': 'drive'},
        {'title': 'Рулевое управление', 'category': 'steering'},
        {'title': 'Подвеска', 'category': 'suspension'},
        {'title': 'Электроника', 'category': 'electronics'},
        {'title': 'Колеса/Шины', 'category': 'wheel'},
        {'title': 'Тормозная система', 'category': 'brakes'},
        {'title': 'Топливная система', 'category': 'fuel'},
        {'title': 'Система охлаждения', 'category': 'cooling'},
    ]

    @staticmethod
    def create_motorcycle(owner_id: int, **kwargs) -> Motorcycle:
        """ Создает мотоцикл с узлами обслуживания """
        motorcycle = Motorcycle(owner_id=owner_id, **kwargs)
        db.session.add(motorcycle)
        db.session.flush()

        for node_data in MotorcycleService.DEFAULT_NODES:
            node = MaintenanceNode(
                moto_id=motorcycle.id,
                title=node_data['title'],
                category=node_data['category']
            )
            db.session.add(node)
        
        db.session.commit()
        return motorcycle
    
    @staticmethod
    def update_motorcycle(moto_id: int, user_id: int, **kwargs) -> Motorcycle:
        """ Обновляет данные мотоцикла """
        moto = MotorcycleService.get_motorcycle_by_id(moto_id, user_id)

        for key, value in kwargs.items():
            if hasattr(moto, key) and value is not None:
                setattr(moto, key, value)

        db.session.commit()

        return moto
    
    @staticmethod
    def update_note(moto_id:int, user_id: int, note_text: str) -> Motorcycle:
        """ Обновляет заметки мотоцикла """
        if len(note_text) > 128:
            raise ValidationError("Длина заметок не более 128 символов")
        
        moto = MotorcycleService.get_motorcycle_by_id(moto_id)
        moto.note = note_text
        db.session.commit()
        return moto
    
    @staticmethod
    def delete_motorcycle(moto_id: int, user_id: int) -> None:
        """ Удаляет мотоцикл """
        moto = MotorcycleService.get_motorcycle_by_id(moto_id, user_id)
        db.session.delete(moto)
        db.session.commit()

    @staticmethod
    def get_user_motorcycles(user_id: int) -> List[Motorcycle]:
        """ Получает все мотоциклы пользователя """
        return Motorcycle.query.filter_by(owner_id=user_id).all()
    
    @staticmethod
    def get_motorcycle_by_id(moto_id: int, user_id: Optional[int] = None) -> Motorcycle:
        """ Получает мотоцикл по ID с проверкой прав"""
        moto = Motorcycle.query.get(moto_id)
        if not moto:
            raise NotFoundError("Мотоцикл не найден")

        if user_id and moto.owner_id != user_id:
            raise ForbiddenError("Вы не являетесь владельцем этого мотоцикла")

        return moto