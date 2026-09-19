from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
import json

from app.exceptions import ValidationError
from app.schemas.manual import (
    CreateManualSchema,
    UpdateManualSchema,
    ManualResponseSchema,
)
from app.services.manual_service import ManualService

manual = Blueprint("manual", __name__)


def _serialize_manual(record) -> dict:
    """Сериализация мануала через Pydantic-схему."""
    return ManualResponseSchema.model_validate(record.to_dict()).model_dump()


@manual.route("/", methods=["GET"])
@jwt_required()
def get_manual_for_maintenance():
    """Получение мануала для конкретного обслуживания."""
    maintenance_id = request.args.get("maintenance_id", type=int)
    moto_id = request.args.get("moto_id", type=int)

    result = ManualService.get_manual_for_maintenance_endpoint(
        maintenance_id=maintenance_id,
        moto_id=moto_id,
        user_id=int(get_jwt_identity()),
    )

    if result is None:
        return jsonify([]), 200

    return jsonify(result), 200


@manual.route("/list", methods=["GET"])
@jwt_required()
def list_manuals():
    """Получение списка мануалов с пагинацией и фильтрами."""
    data = ManualService.list_manuals(
        user_id=int(get_jwt_identity()),
        page=request.args.get("page", 1, type=int),
        per_page=request.args.get("per_page", 8, type=int),
        tab=request.args.get("tab", "all"),
        search=request.args.get("search", ""),
        motorcycle_filter=request.args.get("motorcycle", ""),
        category=request.args.get("category", ""),
        sort_by=request.args.get("sort_by", "created_at_desc"),
        difficult=request.args.get("difficult", ""),
        time_estimate=request.args.get("time_estimate", ""),
        interval=request.args.get("interval", ""),
        status=request.args.get("status", ""),
    )
    data["manuals"] = [
        ManualResponseSchema.model_validate(m).model_dump()
        for m in data["manuals"]
    ]
    return jsonify(data), 200


@manual.route("/<int:manual_id>", methods=["GET"])
@jwt_required()
def get_manual_by_id(manual_id):
    """Получение детальной информации о мануале."""
    manual_record = ManualService.get_manual_for_user(
        manual_id=manual_id,
        user_id=int(get_jwt_identity()),
    )
    return jsonify(_serialize_manual(manual_record)), 200


@manual.route("/new-manual", methods=["POST"])
@jwt_required()
def create_manual():
    """Создание мануала с файлами."""
    data_raw = request.form.get("data")
    if not data_raw:
        raise ValidationError("Данные не переданы")

    try:
        data = json.loads(data_raw)
    except json.JSONDecodeError:
        raise ValidationError("Неверный формат JSON")

    schema = CreateManualSchema.model_validate(data)
    files = request.files.to_dict() if request.files else {}

    created = ManualService.create_manual(
        author_id=int(get_jwt_identity()),
        data=schema.model_dump(),
        files=files,
    )
    return jsonify(_serialize_manual(created)), 201


@manual.route("/<int:manual_id>", methods=["PUT"])
@jwt_required()
def update_manual(manual_id):
    """Обновление мануала."""
    data = UpdateManualSchema.model_validate(request.get_json() or {})

    updated = ManualService.update_manual(
        manual_id=manual_id,
        user_id=int(get_jwt_identity()),
        **data.get_updates(),
    )
    return jsonify(_serialize_manual(updated)), 200


@manual.route("/<int:manual_id>", methods=["DELETE"])
@jwt_required()
def delete_manual(manual_id):
    """
    Удаление мануала
    """
    ManualService.delete_manual(
        manual_id=manual_id,
        user_id=int(get_jwt_identity())
    )
    return jsonify({"message": "Мануал успешно удален"}), 200


@manual.route("/<int:manual_id>/steps/<int:step_id>/image", methods=["POST"])
@jwt_required()
def upload_step_image(manual_id, step_id):
    """Загрузка изображения для шага мануала."""
    if "image" not in request.files:
        raise ValidationError("Файл изображения не найден")

    file = request.files["image"]
    if not file or file.filename == "":
        raise ValidationError("Файл не выбран")

    image_url = ManualService.update_step_image(
        manual_id=manual_id,
        step_id=step_id,
        user_id=int(get_jwt_identity()),
        file=file,
    )
    return jsonify({
        "message": "Изображение загружено",
        "image_url": image_url,
    }), 200


@manual.route("/<int:manual_id>/steps/<int:step_id>/image", methods=["DELETE"])
@jwt_required()
def delete_step_image(manual_id, step_id):
    """Удаление изображения шага."""
    ManualService.delete_step_image(
        manual_id=manual_id,
        step_id=step_id,
        user_id=int(get_jwt_identity()),
    )
    return jsonify({"message": "Изображение удалено"}), 200