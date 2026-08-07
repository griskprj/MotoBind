from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.decorators import moto_owner_required
from app.schemas.motorcycle import (CreateMotorcycleSchema,
                                    UpdateMotorcycleSchema)
from app.services.motorcycle_service import MotorcycleService
from app.utils.helpers import get_current_user_id

motorcycle = Blueprint("motorcycle", __name__)


@motorcycle.route("/", methods=["GET"])
@jwt_required()
def get_user_moto():
    """
    Получение данных о мотоциклах пользователя.
    """
    user_id = get_current_user_id()
    motorcycles = MotorcycleService.get_user_motorcycles(user_id)
    return (
        jsonify(
            [
                m.to_dict(
                    include_maintenance=True,
                    include_planned_maintenance=True,
                    include_maintenance_nodes=True,
                )
                for m in motorcycles
            ]
        ),
        200,
    )


@motorcycle.route("/", methods=["POST"])
@jwt_required()
def create_moto():
    """
    Создание мотоцикла
    """
    data = CreateMotorcycleSchema(**request.get_json())

    moto = MotorcycleService.create_motorcycle(
        owner_id=int(get_jwt_identity()),
        name=data.name,
        years=data.years,
        volume=data.volume,
        mileage=data.mileage,
        color=data.color,
        license_plate=data.licensePlate,
        vin=data.vin,
    )
    return jsonify(moto.to_dict()), 201


@motorcycle.route("/<int:moto_id>", methods=["PUT"])
@jwt_required()
@moto_owner_required
def update_moto(moto_id):
    """
    Обновление мотоцикла
    """
    data = UpdateMotorcycleSchema(**request.get_json())
    user_id = int(get_jwt_identity())
    motorcycle = MotorcycleService.update_motorcycle(
        moto_id=moto_id, user_id=user_id, **data.get_updates()
    )
    return (
        jsonify(
            motorcycle.to_dict(
                include_planned_maintenance=True, include_maintenance=True
            )
        ),
        200,
    )


@motorcycle.route("/<int:moto_id>", methods=["PATCH"])
@jwt_required()
@moto_owner_required
def update_moto_mileage(moto_id):
    """
    Обновление пробега мотоцикла
    """
    data = UpdateMotorcycleSchema(**request.get_json())
    user_id = int(get_jwt_identity())
    motorcycle = MotorcycleService.update_motorcycle(
        moto_id=moto_id, user_id=user_id, **data.get_updates()
    )

    return (
        jsonify(
            motorcycle.to_dict(
                include_planned_maintenance=True, include_maintenance=True
            )
        ),
        200,
    )


@motorcycle.route("/<int:moto_id>/note", methods=["PATCH"])
@jwt_required()
@moto_owner_required
def update_note(moto_id):
    """
    Обновление заметок мотоцикла
    """

    data = request.get_json()

    motorcycle = MotorcycleService.update_note(
        moto_id=moto_id, user_id=int(get_jwt_identity()), note_text=data.get("note")
    )

    return (
        jsonify(
            motorcycle.to_dict(
                include_planned_maintenance=True, include_maintenance=True
            )
        ),
        200,
    )


@motorcycle.route("/<int:moto_id>/photo", methods=["POST"])
@jwt_required()
@moto_owner_required
def upload_moto_photo(moto_id):
    """
    Загрузка фото мотоцикла
    """
    if 'photo' not in request.files:
        return jsonify({"error": "Файл не найден"}), 400
    
    file = request.files['photo']
    if file.filename == '':
        return jsonify({"error": "Файл не выбран"}), 400
    
    user_id = int(get_jwt_identity())
    motorcycle = MotorcycleService.update_moto_photo(moto_id, user_id, file)
    
    return (
        jsonify(
            motorcycle.to_dict(
                include_planned_maintenance=True, include_maintenance=True
            )
        ),
        200,
    )


@motorcycle.route("/<int:moto_id>/photo", methods=["DELETE"])
@jwt_required()
@moto_owner_required
def delete_moto_photo(moto_id):
    """
    Удаление фото мотоцикла
    """
    user_id = int(get_jwt_identity())
    motorcycle = MotorcycleService.delete_moto_photo(moto_id, user_id)
    
    return (
        jsonify(
            motorcycle.to_dict(
                include_planned_maintenance=True, include_maintenance=True
            )
        ),
        200,
    )


@motorcycle.route("/<int:moto_id>", methods=["DELETE"])
@jwt_required()
@moto_owner_required
def delete_moto(moto_id):
    """
    Удаление мотоцикла
    """
    user_id = int(get_jwt_identity())
    MotorcycleService.delete_motorcycle(moto_id, user_id)

    return jsonify({"message": "Мотоцикл удален"}), 200