from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from pydantic import ValidationError

from app.exceptions import ForbiddenError, NotFoundError, ValidationError as AppValidationError
from app.models.maintenance import Maintenance
from app.models.motorcycle import Motorcycle
from app.schemas.maintenance import (
    CreateMaintenanceSchema,
    UpdateMaintenanceSchema,
    MarkMaintenanceAsCompletedSchema,
)
from app.services.maintenance_service import MaintenanceService
from app.services.motorcycle_service import MotorcycleService

maintenance = Blueprint("maintenance", __name__)


@maintenance.route("/", methods=["POST"])
@jwt_required()
def create_maintenance():
    """
    Создание записи обслуживания
    """
    try:
        data = CreateMaintenanceSchema(**request.get_json())
    except ValidationError as e:
        raise AppValidationError(str(e))

    current_user_id = int(get_jwt_identity())

    maintenance = MaintenanceService.create_maintenance(
        author_id=current_user_id,
        moto_id=data.motorcycle_id,
        category=data.category,
        title=data.title,
        description=data.description,
        planned_mileage=data.planned_mileage,
        planned_date=data.planned_date,
        completed_mileage=data.completed_mileage,
        completed_date=data.completed_date,
        cost=data.cost,
    )

    return jsonify(maintenance.to_dict()), 201


@maintenance.route("/<int:maintenance_id>", methods=["PUT"])
@jwt_required()
def update_maintenance(maintenance_id):
    """
    Обновление записи обслуживания
    """
    try:
        data = UpdateMaintenanceSchema(
            maintenance_id=maintenance_id,
            **request.get_json()
        )
    except ValidationError as e:
        raise AppValidationError(str(e))

    current_user_id = int(get_jwt_identity())

    maintenance = MaintenanceService.update_maintenance(
        maintenance_id=maintenance_id,
        user_id=current_user_id,
        **data.get_updates()
    )

    return jsonify(maintenance.to_dict()), 200


@maintenance.route("/<int:maintenance_id>", methods=["DELETE"])
@jwt_required()
def delete_maintenance(maintenance_id):
    """
    Удаление записи обслуживания
    """
    current_user_id = int(get_jwt_identity())

    MaintenanceService.delete_maintenance(
        maintenance_id=maintenance_id,
        user_id=current_user_id
    )

    return jsonify({"message": "Обслуживание удалено"}), 200


@maintenance.route("/<int:maintenance_id>/complete", methods=["POST"])
@jwt_required()
def mark_maintenance_as_completed(maintenance_id):
    """
    Отметить обслуживание как выполненное
    """
    try:
        data = MarkMaintenanceAsCompletedSchema(**request.get_json())
    except ValidationError as e:
        raise AppValidationError(str(e))

    current_user_id = int(get_jwt_identity())
    
    result = MaintenanceService.mark_planned_as_done(
        planned_id=maintenance_id,
        author_id=current_user_id,
        mileage=data.completed_mileage,
        completed_date=data.completed_date,
        cost=data.cost,
        repeat=data.is_repeat,
        interval=data.interval,
        interval_days=data.interval_days,
    )
    
    return jsonify({
        "message": "Обслуживание отмечено как выполненное",
        "maintenance": result["maintenance"].to_dict(),
        "new_planned": result["new_planned"].to_dict() if result.get("new_planned") else None
    }), 200


@maintenance.route("/motorcycle/<int:moto_id>", methods=["GET"])
@jwt_required()
def get_maintenances_by_motorcycle(moto_id):
    """
    Получение всех обслуживаний мотоцикла
    """
    current_user_id = int(get_jwt_identity())

    MotorcycleService.get_motorcycle_by_id(moto_id, current_user_id)

    maintenances = MaintenanceService.get_maintenances_by_motorcycle(
        user_id=current_user_id,
        moto_id=moto_id
    )

    return jsonify([m.to_dict() for m in maintenances]), 200


@maintenance.route("/<int:maintenance_id>", methods=["GET"])
@jwt_required()
def get_maintenance(maintenance_id):
    """
    Получение конкретного обслуживания
    """
    current_user_id = int(get_jwt_identity())

    maintenance = MaintenanceService.get_maintenance_by_id(
        user_id=current_user_id,
        maintenance_id=maintenance_id
    )

    return jsonify(maintenance.to_dict()), 200