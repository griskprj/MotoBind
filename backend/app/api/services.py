from app.decorators import business_owner_required
from app.schemas.service import (
    CreateServiceSchema,
    RejectServiceSchema,
    UpdateServiceSchema,
)
from app.services.service_service import ServiceService
from app.utils.helpers import get_current_user_id
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

services = Blueprint("services", __name__)


# ============================================================
# МАСТЕР / СТО
# ============================================================


@services.route("/", methods=["GET"])
@jwt_required()
@business_owner_required
def list_my_services():
    """Список моих услуг (все статусы)."""
    items = ServiceService.list_for_user(get_current_user_id())
    return jsonify([s.to_dict() for s in items]), 200


@services.route("/", methods=["POST"])
@jwt_required()
@business_owner_required
def create_service():
    """Создать услугу. Уходит на модерацию."""
    data = CreateServiceSchema.model_validate(request.get_json() or {})

    service = ServiceService.create(
        user_id=get_current_user_id(),
        title=data.title,
        description=data.description,
        category=data.category,
        price_from=data.price_from,
        price_to=data.price_to,
        duration_min=data.duration_min,
    )
    return jsonify(service.to_dict()), 201


@services.route("/<int:service_id>", methods=["PUT"])
@jwt_required()
@business_owner_required
def update_service(service_id):
    """Обновить услугу. Сбрасывает в pending."""
    data = UpdateServiceSchema.model_validate(request.get_json() or {})

    service = ServiceService.update(
        user_id=get_current_user_id(),
        service_id=service_id,
        **data.get_updates(),
    )
    return jsonify(service.to_dict()), 200


@services.route("/<int:service_id>", methods=["DELETE"])
@jwt_required()
@business_owner_required
def delete_service(service_id):
    ServiceService.delete(get_current_user_id(), service_id)
    return jsonify({"message": "Услуга удалена"}), 200


# ============================================================
# ПУБЛИЧНОЕ
# ============================================================


@services.route("/public/<string:slug>", methods=["GET"])
def list_public_services(slug):
    """Публичный список одобренных услуг мастера."""
    items = ServiceService.list_public_for_slug(slug)
    return jsonify([s.to_dict() for s in items]), 200
