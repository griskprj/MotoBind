from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.extensions import db
from app.schemas.event import CreateEventSchema, UpdateEventSchema, UpdateEventStatusSchema
from app.services.event_service import EventService
from app.exceptions import NotFoundError, ValidationError

event = Blueprint('event', __name__)


@event.route('/', methods=['POST'])
@jwt_required()
def create_event():
    """
    Создает мероприятияе
    """

    data = CreateEventSchema(**request.get_json())
    
    event = EventService.craete_event(
        author_id=int(get_jwt_identity()),
        title=data.title,
        description=data.description,
        status='moderate',
        date=data.date
    )

    return jsonify(event.to_dict(include_subscriptions=False)), 201

@event.route('/<int:event_id>', methods=['PUT'])
@jwt_required()
def update_event(event_id):
    """
    Обновляет мероприятие
    """

    data = UpdateEventSchema(**request.get_json())
    updates = data.get_updates()
    if not updates:
        raise ValidationError("Нет обновленных полей")
    
    event = EventService.update_event(
        user_id=int(get_jwt_identity()),
        event_id=event_id,
        **updates
    )

    return jsonify(event.to_dict(include_subscriptions=False)), 200

@event.route('/<int:event_id>', methods=['GET'])
@jwt_required()
def get_event(event_id):
    """
    Возвращает мероприятие по ID
    """
    event = EventService.get_event_by_id(event_id)
    return jsonify(event.to_dict(include_subscriptions=True)), 200

@event.route('/', methods=['GET'])
@jwt_required()
def get_all_events():
    """
    Возвращает все мероприятия
    """
    events = EventService.get_all_events()
    return jsonify(events), 200

@event.route('/<int:event_id>', methods=['DELETE'])
@jwt_required()
def delete_event(event_id):
    """
    Удалить мероприятие
    """

    event = EventService.get_event_by_id(event_id)
    db.session.delete(event)
    db.session.commit()

    return jsonify({
        'message': 'Мероприятие удалено'
    }), 200

@event.route('/<int:event_id>', methods=['PATCH'])
@jwt_required()
def change_event_status(event_id):
    """
    Изменить статус мероприятия
    """

    data = UpdateEventStatusSchema(**request.get_json())
    event = EventService.update_event_status(
        event_id=event_id,
        user_id=int(get_jwt_identity()),
        status=data.status
    )

    return jsonify(event.to_dict(include_subscriptions=True)), 200

@event.route('/<int:event_id>/sub', methods=['POST'])
@jwt_required()
def sub_on_event(event_id):
    """
    Записаться на мероприятие
    """

    event = EventService.get_event_by_id(event_id)
    event = EventService.sub_on_event(
        event_id=event_id,
        user_id=int(get_jwt_identity())
    )

    return jsonify(event.to_dict(include_subscriptions=True)), 201

@event.route('/<int:event_id>/unsub', methods=['POST'])
@jwt_required()
def unsub_from_event(event_id):
    """
    Отписаться от мероприятия
    """

    event = EventService.get_event_by_id(event_id)
    event = EventService.unsub_from_event(
        event_id=event_id,
        user_id=int(get_jwt_identity())
    )

    return jsonify(event.to_dict(include_subscriptions=True)), 201