from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from app.schemas.maintenance import (
    CreateMaintenanceSchema,
    MaintenanceResponseSchema,
    UpdateMaintenanceSchema,
    MarkMaintenanceAsCompletedSchema,
    QuickStartSchema,
)
from app.services.maintenance_service import MaintenanceService
from app.utils.helpers import get_current_user_id

maintenance = Blueprint("maintenance", __name__)


def _serialize(record) -> dict:
    """Сериализация через Pydantic-схему"""
    return MaintenanceResponseSchema.model_validate(record).model_dump()


@maintenance.route("/", methods=["POST"])
@jwt_required()
def create_maintenance():
    """Создание записи обслуживания."""
    data = CreateMaintenanceSchema.model_validate(request.get_json() or {})

    record = MaintenanceService.create_maintenance(
        author_id=get_current_user_id(),
        moto_id=data.motorcycle_id,
        category=data.category,
        title=data.title,
        description=data.description,
        planned_mileage=data.planned_mileage,
        planned_date=data.planned_date,
        completed_date=data.completed_date,
        completed_mileage=data.completed_mileage,
        cost=data.cost,
    )
    return jsonify(_serialize(record)), 201

@maintenance.route("/<int:maintenance_id>", methods=["PUT"])
@jwt_required()
def update_maintenance(maintenance_id):
    """Обновляет записи обслуживания."""
    payload = request.get_json() or {}
    payload["maintenanceId"] = maintenance_id
    data = UpdateMaintenanceSchema.model_validate(payload)

    record = MaintenanceService.update_maintenance(
        maintenance_id=maintenance_id,
        user_id=get_current_user_id(),
        **data.get_updates(),
    )
    return jsonify(_serialize(record)), 200

@maintenance.route("/<int:maintenance_id>", methods=["DELETE"])
@jwt_required()
def delete_maintenance(maintenance_id):
    """Удаление записи обслуживания."""
    MaintenanceService.delete_maintenance(
        maintenance_id=maintenance_id,
        user_id=get_current_user_id(),
    )
    return jsonify({"message": "Обслуживание удалено"}), 200

@maintenance.route("/<int:maintenance_id>/complete", methods=["POST"])
@jwt_required()
def mark_maintenance_as_completed(maintenance_id):
    """Отметить обслуживание как выполненное."""
    data = MarkMaintenanceAsCompletedSchema.model_validate(
        request.get_json() or {}
    )

    result = MaintenanceService.mark_planned_as_done(
        planned_id=maintenance_id,
        author_id=get_current_user_id(),
        mileage=data.completed_mileage,
        completed_date=data.completed_date,
        cost=data.cost,
        repeat=data.is_repeat,
        interval=data.interval,
        interval_days=data.interval_days,
    )
    return jsonify({
        "message": "Обслуживание отмечено как выполненное",
        "maintenance": _serialize(result["maintenance"]),
        "new_planned": _serialize(result["new_planned"]) if result.get("new_planned") else None,
    }), 200

@maintenance.route("/motorcycle/<int:moto_id>", methods=["GET"])
@jwt_required()
def get_maintenances_by_motorcycle(moto_id):
    """Получение всех обслуживаний мотоцикла."""
    records = MaintenanceService.get_maintenances_by_motorcycle(
        user_id=get_current_user_id(),
        moto_id=moto_id,
    )
    return jsonify([_serialize(r) for r in records]), 200

@maintenance.route("/<int:maintenance_id>", methods=["GET"])
@jwt_required()
def get_maintenance(maintenance_id):
    """Получение конкретного обслуживания."""
    record = MaintenanceService.get_maintenance_by_id(
        user_id=get_current_user_id(),
        maintenance_id=maintenance_id
    )
    return jsonify(_serialize(record)), 200

@maintenance.route("/quick-start", methods=["POST"])
@jwt_required()
def quick_start():
    """Быстрое создание базовых обслуживаний для мотоцикла."""
    data = QuickStartSchema.model_validate(request.get_json() or {})

    result = MaintenanceService.quick_start(
        user_id=get_current_user_id(),
        moto_id=data.moto_id,
        current_mileage=data.current_mileage,
        drive_type=data.drive_type,
        style=data.style,
        terrain=data.terrain,
    )
    return jsonify(result), 201