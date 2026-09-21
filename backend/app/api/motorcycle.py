from app.decorators import moto_owner_required
from app.schemas.motorcycle import (
    CreateMotorcycleSchema,
    MotorcycleDetailSchema,
    MotorcycleShortSchema,
    UpdateMotorcycleSchema,
)
from app.services.motorcycle_service import MotorcycleService
from app.utils.helpers import get_current_user_id
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

motorcycle = Blueprint("motorcycle", __name__)


def _serialize_short(moto) -> dict:
    """Базовый ответ без ТО."""
    return MotorcycleShortSchema.model_validate(moto).model_dump()


def _serialize_detail(moto) -> dict:
    """Ответ с вложенным ТО."""
    return MotorcycleDetailSchema.model_validate(moto).model_dump()


@motorcycle.route("/", methods=["GET"])
@jwt_required()
def get_user_motos():
    """
    Получение данных о мотоциклах пользователя.
    """
    user_id = get_current_user_id()
    motorcycles = MotorcycleService.get_user_motorcycles(user_id)
    return jsonify([_serialize_detail(m) for m in motorcycles]), 200


@motorcycle.route("/<int:moto_id>", methods=["GET"])
@jwt_required()
def get_user_moto(moto_id):
    """
    Получение данных о конкретном мотоцикле пользователя.
    """
    user_id = get_current_user_id()
    motorcycle = MotorcycleService.get_motorcycle_by_id(moto_id, user_id)
    return jsonify(_serialize_detail(motorcycle)), 200


@motorcycle.route("/", methods=["POST"])
@jwt_required()
def create_moto():
    """Создание мотоцикла."""
    data = CreateMotorcycleSchema.model_validate(request.get_json() or {})

    moto = MotorcycleService.create_motorcycle(
        owner_id=get_current_user_id(),
        name=data.name,
        years=data.years,
        volume=data.volume,
        mileage=data.mileage,
        color=data.color,
        license_plate=data.license_plate,
        vin=data.vin,
    )
    return jsonify(_serialize_short(moto)), 201


@motorcycle.route("/<int:moto_id>", methods=["PUT"])
@jwt_required()
@moto_owner_required
def update_moto(moto_id):
    """Обновление мотоцикла."""
    data = UpdateMotorcycleSchema.model_validate(request.get_json() or {})
    updated = MotorcycleService.update_motorcycle(
        moto_id=moto_id,
        user_id=get_current_user_id(),
        **data.get_updates(),
    )
    return jsonify(_serialize_detail(updated)), 200


@motorcycle.route("/<int:moto_id>", methods=["PATCH"])
@jwt_required()
@moto_owner_required
def update_moto_mileage(moto_id):
    """Обновление пробега мотоцикла."""
    data = UpdateMotorcycleSchema.model_validate(request.get_json() or {})
    updated = MotorcycleService.update_motorcycle_mileage(
        moto_id=moto_id,
        user_id=get_current_user_id(),
        mileage=data.mileage,
    )
    return jsonify(_serialize_detail(updated)), 200


@motorcycle.route("/<int:moto_id>/note", methods=["PATCH"])
@jwt_required()
@moto_owner_required
def update_note(moto_id):
    """Обновление заметок мотоцикла."""
    data = request.get_json() or {}
    updated = MotorcycleService.update_note(
        moto_id=moto_id,
        user_id=get_current_user_id(),
        note_text=data.get("note"),
    )
    return jsonify(_serialize_detail(updated)), 200


@motorcycle.route("/<int:moto_id>/photo", methods=["POST"])
@jwt_required()
@moto_owner_required
def upload_moto_photo(moto_id):
    """Загрузка фото мотоцикла."""
    if "photo" not in request.files:
        return jsonify({"error": "Файл не найден"}), 400

    file = request.files["photo"]
    if file.filename == "":
        return jsonify({"error": "Файл не выбран"}), 400

    updated = MotorcycleService.update_moto_photo(moto_id, get_current_user_id(), file)

    return jsonify(_serialize_detail(updated)), 200


@motorcycle.route("/<int:moto_id>/photo", methods=["DELETE"])
@jwt_required()
@moto_owner_required
def delete_moto_photo(moto_id):
    """Удаление фото мотоцикла."""
    updated = MotorcycleService.delete_moto_photo(moto_id, get_current_user_id())

    return jsonify(_serialize_detail(updated)), 200


@motorcycle.route("/<int:moto_id>", methods=["DELETE"])
@jwt_required()
@moto_owner_required
def delete_moto(moto_id):
    """Удаление мотоцикла."""
    MotorcycleService.delete_motorcycle(moto_id, get_current_user_id())
    return jsonify({"message": "Мотоцикл удален"}), 200
