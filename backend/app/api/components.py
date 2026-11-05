from datetime import datetime

from app.exceptions import ValidationError
from app.schemas.component import (
    ApplyTemplateResponseSchema,
    ApplyTemplateSchema,
    ComponentHistoryItemSchema,
    ComponentHistoryResponseSchema,
    ComponentListResponseSchema,
    ComponentResponseSchema,
    CreateComponentSchema,
    UpdateComponentSchema,
)
from app.services.component_service import ComponentService
from app.utils.helpers import get_current_user_id
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

components = Blueprint("components", __name__)


def _parse_date(value: str | None):
    if value is None or value == "":
        return None
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError:
        raise ValidationError("Неверный формат даты. Используйте ГГГГ-ММ-ДД")


def _serialize(component) -> dict:
    return ComponentResponseSchema.model_validate(component).model_dump()


# ============================================================
# СПИСОК / СОЗДАНИЕ
# ============================================================


@components.route("/", methods=["GET"])
@jwt_required()
def list_components(moto_id):
    user_id = get_current_user_id()
    include_inactive = request.args.get("include_inactive", "false").lower() == "true"

    items = ComponentService.list_for_motorcycle(
        user_id=user_id, moto_id=moto_id, include_inactive=include_inactive
    )
    payload = ComponentListResponseSchema(
        components=[ComponentResponseSchema.model_validate(c) for c in items],
        total=len(items),
    ).model_dump()
    return jsonify(payload), 200


@components.route("/", methods=["POST"])
@jwt_required()
def create_component(moto_id):
    user_id = get_current_user_id()
    data = CreateComponentSchema.model_validate(request.get_json() or {})

    component = ComponentService.create(
        user_id=user_id,
        moto_id=moto_id,
        name=data.name,
        category=data.category,
        manufacturer=data.manufacturer,
        part_number=data.part_number,
        interval_km=data.interval_km,
        interval_days=data.interval_days,
        last_service_date=_parse_date(data.last_service_date),
        last_service_mileage=data.last_service_mileage,
        condition_rating=data.condition_rating,
        condition_note=data.condition_note,
    )
    return jsonify(_serialize(component)), 201


# ============================================================
# БАЗОВЫЙ НАБОР
# ============================================================


@components.route("/apply-template", methods=["POST"])
@jwt_required()
def apply_template(moto_id):
    user_id = get_current_user_id()
    data = ApplyTemplateSchema.model_validate(request.get_json() or {})

    result = ComponentService.apply_template(
        user_id=user_id,
        moto_id=moto_id,
        style=data.style,
        terrain=data.terrain,
    )
    payload = ApplyTemplateResponseSchema.model_validate(result).model_dump()
    return jsonify(payload), 201


# ============================================================
# КОНКРЕТНЫЙ КОМПОНЕНТ
# ============================================================


@components.route("/<int:component_id>", methods=["GET"])
@jwt_required()
def get_component(moto_id, component_id):
    user_id = get_current_user_id()
    include_inactive = request.args.get("include_inactive", "false").lower() == "true"

    component = ComponentService.get_by_id(
        user_id=user_id,
        moto_id=moto_id,
        component_id=component_id,
        include_inactive=include_inactive,
    )
    return jsonify(_serialize(component)), 200


@components.route("/<int:component_id>", methods=["PUT"])
@jwt_required()
def update_component(moto_id, component_id):
    user_id = get_current_user_id()
    data = UpdateComponentSchema.model_validate(request.get_json() or {})

    updates = data.get_updates()
    if "last_service_date" in updates:
        updates["last_service_date"] = _parse_date(updates["last_service_date"])

    component = ComponentService.update(
        user_id=user_id,
        moto_id=moto_id,
        component_id=component_id,
        **updates,
    )
    return jsonify(_serialize(component)), 200


@components.route("/<int:component_id>", methods=["DELETE"])
@jwt_required()
def deactivate_component(moto_id, component_id):
    user_id = get_current_user_id()
    ComponentService.deactivate(
        user_id=user_id, moto_id=moto_id, component_id=component_id
    )
    return jsonify({"message": "Компонент удалён из списка"}), 200


@components.route("/<int:component_id>/reactivate", methods=["POST"])
@jwt_required()
def reactivate_component(moto_id, component_id):
    user_id = get_current_user_id()
    component = ComponentService.reactivate(
        user_id=user_id, moto_id=moto_id, component_id=component_id
    )
    return jsonify(_serialize(component)), 200


# ============================================================
# ИСТОРИЯ
# ============================================================


@components.route("/<int:component_id>/history", methods=["GET"])
@jwt_required()
def get_component_history(moto_id, component_id):
    user_id = get_current_user_id()

    works = ComponentService.get_history(
        user_id=user_id, moto_id=moto_id, component_id=component_id
    )

    items = []
    for w in works:
        item = ComponentHistoryItemSchema.model_validate(w).model_dump()
        if w.event is not None:
            item["event"] = {
                "id": w.event.id,
                "date": w.event.date.isoformat() if w.event.date else None,
                "mileage": w.event.mileage,
                "comment": w.event.comment,
            }
        items.append(item)

    component = ComponentService.get_by_id(
        user_id=user_id,
        moto_id=moto_id,
        component_id=component_id,
        include_inactive=True,
    )
    payload = ComponentHistoryResponseSchema(
        component=ComponentResponseSchema.model_validate(component),
        history=[ComponentHistoryItemSchema.model_validate(i) for i in items],
    ).model_dump()
    return jsonify(payload), 200
