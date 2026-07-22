from datetime import datetime
from typing import Optional, Dict, Any
from app.models.event import Event
from app.models.user import User
from app.extensions import db
from app.exceptions import NotFoundError, ForbiddenError, ValidationError


class EventService:
    """ Сервис для работы с мероприятиями """

    @staticmethod
    def craete_event(
        author_id: int,
        title: int,
        description: str,
        status: str,
        date: Optional[datetime] = None
    ) -> Event:
        """ Создает мероприятияе """
        if not(User.query.get(author_id)):
            raise NotFoundError("Пользователь не найден")
        
        event = Event(
            author_id=author_id,
            title=title,
            description=description,
            status=status,
            date=date
        )
        db.session.add(event)
        db.session.commit()

        return event
    
    @staticmethod
    def update_event(event_id: int, user_id: int, **kwargs) ->Event:
        """ Обновляет данные запланированного обслуживания """
        event = EventService.get_event_by_id(event_id)
        if event.author_id != user_id:
            raise ForbiddenError("Вы не являетесь автором этого мероприятия")

        for key, value in kwargs.items():
            if hasattr(event, key) and value is not None:
                setattr(event, key, value)
        
        db.session.commit()
        return event
    
    @staticmethod
    def delete_event(event_id: int, user_id: int) -> None:
        """ Удаляет мероприятие """
        event = EventService.get_event_by_id(event_id)
        if event.author_id != user_id:
            raise ForbiddenError("Вы можете удалять только свои мероприятия")
        db.session.delete(event)
        db.session.commit()

    
    @staticmethod
    def update_event_status(event_id: int, user_id: int, status: str) -> Event:
        """ Обновляет статус мероприятия """
        event = EventService.get_event_by_id(event_id)
        if event.author_id != user_id:
            raise ForbiddenError("Вы можете изменять статус только для своих мероприятий")
        
        allowed = ['moderate', 'planned', 'active', 'complete']
        if status not in allowed:
            raise ValidationError(f"Статус должен быть одним из этих: {', '.join(allowed)}")
        
        event.status = status
        db.session.commit()
        return event
    
    
    @staticmethod
    def sub_on_event(event_id: int, user_id: int) -> Event:
        """ Записаться на мероприятие """
        event = EventService.get_event_by_id(event_id)
        user = User.query.get(user_id)
        if not user:
            raise NotFoundError("Пользователь не найден")
        
        if user in event.subscriptions:
            raise ForbiddenError("Вы уже записаны на это мероприятие")
        
        event.subscriptions.append(user)
        db.session.commit()
        return event

    @staticmethod
    def unsub_from_event(event_id: int, user_id: int) -> Event:
        """ Отписаться от мероприятия """
        event = EventService.get_event_by_id(event_id)
        user = User.query.get(user_id)
        if not user:
            raise NotFoundError("Пользователь не найден")
        
        if user not in event.subscriptions:
            raise ForbiddenError("Вы не записаны на мероприятие")
        
        event.subscriptions.remove(user)
        db.session.commit()
        return event

    @staticmethod
    def get_event_subscribers(event_id: int) -> list:
        """ Получить список подписчиков мероприятия """
        event = EventService.get_event_by_id(event_id)
        return event.subscriptions

    @staticmethod
    def get_event_by_id(event_id: int) -> Event:
        """ Получить мероприятияе по ID """
        event = Event.query.get(event_id)
        if not event:
            raise NotFoundError("Мероприятие не найдено")
        
        return event