from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from pydantic import ValidationError
from datetime import datetime, timedelta

from app.extensions import db
from app.exceptions import ValidationError as AppValidationError
from app.schemas.maintenance import (
    CreateMaintenanceSchema,
    UpdateMaintenanceSchema,
    MarkMaintenanceAsCompletedSchema,
)
from app.models.maintenance import Maintenance
from app.services.maintenance_service import MaintenanceService
from app.services.motorcycle_service import MotorcycleService
from app.services.notification_service import NotificationService
from app.constants.maintenance_presets import (
    get_presets_for_motorcycle,
    calculate_interval
)

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


@maintenance.route('/quick-start', methods=['POST'])
@jwt_required()
def quick_start():
    """
    Быстрое создание базовых обслуживаний для мотоцикла
    """
    user_id = int(get_jwt_identity())
    data = request.get_json()

    moto_id = data.get('moto_id')
    current_mileage = data.get('current_mileage')
    drive_type = data.get('drive_type', 'chain')
    style = data.get('style', 'normal')
    terrain = data.get('terrain', 'mixed')

    if not moto_id:
        raise ValidationError('Не указан мотоцикл')

    moto = MotorcycleService.get_motorcycle_by_id(moto_id=moto_id, user_id=user_id)

    if not current_mileage or current_mileage < 0:
        raise ValidationError('Некорректный пробег')

    existing = Maintenance.query.filter_by(moto_id=moto_id).count()
    if existing > 0:
        raise ValidationError('У мотоцикла уже есть обслуживания')

    moto.mileage = current_mileage
    if hasattr(moto, 'drive_type'):
        moto.drive_type = drive_type

    presets = get_presets_for_motorcycle(drive_type)

    today = datetime.utcnow().date()
    created = []

    for preset in presets:
        interval = calculate_interval(preset, style, terrain)

        planned_mileage = current_mileage + interval['interval_km']
        planned_date = today + timedelta(days=interval['interval_days'])

        maintenance = Maintenance(
            moto_id=moto_id,
            author_id=user_id,
            title=preset['title'],
            description=preset['description'],
            category=preset['category'],
            status='planned',
            planned_mileage=planned_mileage,
            planned_date=planned_date
        )

        db.session.add(maintenance)
        created.append({
            'title': preset['title'],
            'planned_mileage': planned_mileage,
            'planned_date': planned_date.isoformat(),
            'interval_km': interval['interval_km']
        })

    db.session.commit()

    NotificationService.send_notification(
        user_id=user_id,
        type='system',
        title='Базовое обслуживание создано',
        content=f'Для {moto.name} создано {len(created)} плановых работ',
        link='/maintenance'
    )

    return jsonify({
        'message': f'Создано {len(created)} обслуживаний',
        'created': created,
        'moto': moto.to_dict()
    }), 201