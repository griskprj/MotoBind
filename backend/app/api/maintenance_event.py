from app.schemas.maintenance_event import (
    CreateEventSchema,
    EventListResponseSchema,
    EventResponseSchema,
    UpdateEventSchema,
)
from app.services.event_service import EventService
from app.utils.helpers import get_current_user_id
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

maintenance_events = Blueprint("maintenance_events", __name__)


def _serialize(event) -> dict:
    return EventResponseSchema.model_validate(event).model_dump()


@maintenance_events.route("/", methods=["POST"])
@jwt_required()
def create_event():
    data = CreateEventSchema.model_validate(request.get_json() or {})
    event = EventService.create(
        user_id=get_current_user_id(),
        moto_id=data.motorcycle_id,
        date_str=data.date,
        mileage=data.mileage,
        total_cost=data.total_cost,
        comment=data.comment,
        works=[w.model_dump() for w in data.works],
    )
    return jsonify(_serialize(event)), 201


@maintenance_events.route("/", methods=["GET"])
@jwt_required()
def list_events():
    moto_id = request.args.get("motorcycle_id", type=int)
    if not moto_id:
        from app.exceptions import ValidationError

        raise ValidationError("Параметр motorcycle_id обязателен")

    data = EventService.list_for_motorcycle(
        user_id=get_current_user_id(),
        moto_id=moto_id,
        page=request.args.get("page", 1, type=int),
        per_page=request.args.get("per_page", 20, type=int),
    )
    payload = EventListResponseSchema(
        events=[EventResponseSchema.model_validate(e) for e in data["events"]],
        total=data["total"],
        page=data["page"],
        per_page=data["per_page"],
        pages=data["pages"],
    ).model_dump()
    return jsonify(payload), 200


@maintenance_events.route("/<int:event_id>", methods=["GET"])
@jwt_required()
def get_event(event_id):
    moto_id = request.args.get("motorcycle_id", type=int)
    if not moto_id:
        from app.exceptions import ValidationError

        raise ValidationError("Параметр motorcycle_id обязателен")
    event = EventService.get_by_id(get_current_user_id(), moto_id, event_id)
    return jsonify(_serialize(event)), 200


@maintenance_events.route("/<int:event_id>", methods=["PUT"])
@jwt_required()
def update_event(event_id):
    data = UpdateEventSchema.model_validate(request.get_json() or {})
    moto_id = request.args.get("motorcycle_id", type=int)
    if not moto_id:
        from app.exceptions import ValidationError

        raise ValidationError("Параметр motorcycle_id обязателен")

    updates = data.get_updates()
    if "works" in updates and updates["works"] is not None:
        updates["works"] = [
            w.model_dump() if hasattr(w, "model_dump") else w for w in updates["works"]
        ]
    event = EventService.update(get_current_user_id(), moto_id, event_id, **updates)
    return jsonify(_serialize(event)), 200


@maintenance_events.route("/<int:event_id>", methods=["DELETE"])
@jwt_required()
def delete_event(event_id):
    moto_id = request.args.get("motorcycle_id", type=int)
    if not moto_id:
        from app.exceptions import ValidationError

        raise ValidationError("Параметр motorcycle_id обязателен")
    EventService.delete(get_current_user_id(), moto_id, event_id)
    return jsonify({"message": "Событие удалено"}), 200
