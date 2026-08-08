from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from datetime import datetime

from app.exceptions import ValidationError
from app.schemas.maintenance import (CreateMaintenanceSchema,
                                     CreatePlannedMaintenanceSchema,
                                     MarkPlannedMaintenanceSchema,
                                     UpdatePlannedMaintenanceSchema)
from app.services.maintenance_service import MaintenanceService
from app.utils.helpers import check_motorcycle_owner, get_current_user

maintenance = Blueprint("maintenance", __name__)


@maintenance.route("/history", methods=["POST"])
@jwt_required()
def create_maintenance():
    """
    Создание записи обслуживания
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
        mileage=data.mileage,
        cost=data.cost,
        date=data.date,
    )

    return jsonify(maintenance), 201


@maintenance.route("/plan", methods=["POST"])
@jwt_required()
def create_planned_maintenance():
    """
    Планирование обслуживания
    """
    data = CreatePlannedMaintenanceSchema(**request.get_json())

    planned_maintenance = MaintenanceService.create_planned_maintenance(
        author_id=int(get_jwt_identity()),
        moto_id=data.motorcycle_id,
        title=data.title,
        description=data.description,
        category=data.category,
        planned_mileage=data.planned_mileage,
    )

    return jsonify(planned_maintenance), 201


@maintenance.route("/plan", methods=["PUT"])
@jwt_required()
def update_planned_maintenance():
    """
    Редактирование планового обслуживания
    """
    data = UpdatePlannedMaintenanceSchema(**request.get_json())
    updates = data.get_updates()
    if not updates:
        raise ValidationError("Нет данных для обновления")

    user_id = int(get_jwt_identity())
    planned_maintenance = MaintenanceService.update_planned_maintenance(
        maintenance_id=data.maintenance_id, user_id=user_id, **updates
    )

    return jsonify(planned_maintenance.to_dict()), 200


@maintenance.route("/plan/<int:maintenance_id>", methods=["DELETE"])
@jwt_required()
def delete_planned_maintenance(maintenance_id):
    """
    Удаление планового обслуживания
    """
    user_id = int(get_jwt_identity())
    MaintenanceService.delete_plan_maintenance(maintenance_id, user_id)

    return jsonify({"message": "Запись удалена"}), 200


@maintenance.route("/<int:maintenance_id>", methods=["DELETE"])
@jwt_required()
def delete_maintenance(maintenance_id):
    """
    Удаление обслуживания
    """
    user_id = int(get_jwt_identity())
    MaintenanceService.delete_maintenance(maintenance_id, user_id)

    return jsonify({"message": "Запись удалена"}), 200


@maintenance.route("/plan/mark", methods=["POST"])
@jwt_required()
def mark_planned_as_done():
    """
    Отметка о выполнении планового обслуживания
    """

    data = MarkPlannedMaintenanceSchema(**request.get_json())
    current_user_id = int(get_jwt_identity())
    result = MaintenanceService.mark_planned_as_done(
        planned_id=data.maintenance_id,
        author_id=current_user_id,
        mileage=data.mileage,
        date=data.date,
        cost=data.cost,
        repeat=data.is_repeat,
        interval=data.interval,
    )

    return (
        jsonify(
            {
                "message": "Обслуживание отмечено как выполненное",
                "new_maintenance": result["new_planned"],
            }
        ),
        201,
    )


@maintenance.route("/nodes/<int:moto_id>", methods=["GET"])
@jwt_required()
def get_maintenance_nodes(moto_id):
    """
    Получение узлов обслуживания мотоцикла
    """
    user_id = int(get_jwt_identity())
    nodes = MaintenanceService.get_maintenanc_nodes(user_id, moto_id)
    return jsonify(nodes), 200
