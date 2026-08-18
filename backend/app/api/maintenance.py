from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.exceptions import ValidationError
from app.schemas.maintenance import (
    CreateMaintenanceSchema,
    UpdateMaintenanceSchema,
    MarkMaintenanceAsCompletedSchema
)
from app.services.maintenance_service import MaintenanceService
from app.utils.helpers import check_motorcycle_owner, get_current_user

maintenance = Blueprint("maintenance", __name__)


@maintenance.route("/", methods=["POST"])
@jwt_required()
def create_maintenance():
    """
    Создание записи обслуживания (плановой или выполненной)
    """
    data = CreateMaintenanceSchema(**request.get_json())
    user = get_current_user()
    check_motorcycle_owner(data.motorcycle_id, user.id)

    maintenance = MaintenanceService.create_maintenance(
        author_id=user.id,
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
    Редактирование обслуживания
    """
    data = UpdateMaintenanceSchema(**request.get_json())
    updates = data.get_updates()
    
    if not updates:
        raise ValidationError("Нет данных для обновления")

    user_id = int(get_jwt_identity())
    maintenance = MaintenanceService.update_maintenance(
        maintenance_id=maintenance_id, 
        user_id=user_id, 
        **updates
    )

    return jsonify(maintenance.to_dict()), 200


@maintenance.route("/<int:maintenance_id>/complete", methods=["POST"])
@jwt_required()
def mark_maintenance_as_completed(maintenance_id):
    """
    Отметка планового ТО как выполненного
    """
    data = MarkMaintenanceAsCompletedSchema(**request.get_json())
    current_user_id = int(get_jwt_identity())
    
    result = MaintenanceService.mark_planned_as_done(
        planned_id=maintenance_id,
        author_id=current_user_id,
        mileage=data.completed_mileage,
        date=data.completed_date,
        cost=data.cost,
        repeat=data.is_repeat,
        interval=data.interval,
    )

    response = {
        "message": "Обслуживание отмечено как выполненное",
        "maintenance": result["maintenance"].to_dict() if result["maintenance"] else None,
    }
    if result.get("new_planned"):
        response["new_planned"] = result["new_planned"].to_dict()

    return jsonify(response), 200


@maintenance.route("/<int:maintenance_id>", methods=["DELETE"])
@jwt_required()
def delete_maintenance(maintenance_id):
    """
    Удаление обслуживания
    """
    user_id = int(get_jwt_identity())
    MaintenanceService.delete_maintenance(maintenance_id, user_id)

    return jsonify({"message": "Запись удалена"}), 200


@maintenance.route("/motorcycle/<int:moto_id>", methods=["GET"])
@jwt_required()
def get_motorcycle_maintenances(moto_id):
    """
    Получение всех обслуживаний мотоцикла
    """
    user_id = int(get_jwt_identity())
    check_motorcycle_owner(moto_id, user_id)
    
    maintenances = MaintenanceService.get_maintenances_by_motorcycle(user_id, moto_id)
    return jsonify([m.to_dict() for m in maintenances]), 200