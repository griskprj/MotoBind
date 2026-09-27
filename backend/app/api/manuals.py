import json

from app.exceptions import ValidationError
from app.schemas.manual import (
    CreateManualSchema,
    ManualResponseSchema,
    UpdateManualSchema,
)
from app.services.manual_service import ManualService
from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required, verify_jwt_in_request
from flask_jwt_extended.exceptions import NoAuthorizationError

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


def _optional_user_id():
    """
    Возвращает user_id, если передан валидный JWT, иначе None.
    Не бросает исключений — используется на публичных роутах.
    """
    try:
        verify_jwt_in_request(optional=True)
        identity = get_jwt_identity()
        return int(identity) if identity else None
    except NoAuthorizationError:
        return None
    except Exception:
        return None


@manual.route("/list", methods=["GET"])
def list_manuals():
    """
    Публичный список мануалов.

    Для гостей принудительно:
      - tab = 'all'
      - status = 'approved'
      - игнорируются 'my' и 'myMotos'
    """
    user_id = _optional_user_id()
    is_guest = user_id is None

    tab = request.args.get("tab", "all")
    status = request.args.get("status", "")

    if is_guest:
        tab = "all"
        status = "approved"

    data = ManualService.list_manuals(
        user_id=user_id or 0,
        page=request.args.get("page", 1, type=int),
        per_page=request.args.get("per_page", 8, type=int),
        tab=tab,
        search=request.args.get("search", ""),
        motorcycle_filter=request.args.get("motorcycle", ""),
        category=request.args.get("category", ""),
        sort_by=request.args.get("sort_by", "created_at_desc"),
        difficult=request.args.get("difficult", ""),
        time_estimate=request.args.get("time_estimate", ""),
        interval=request.args.get("interval", ""),
        status=status,
    )

    data["manuals"] = [
        ManualResponseSchema.model_validate(m).model_dump() for m in data["manuals"]
    ]
    return jsonify(data), 200


@manual.route("/<int:manual_id>", methods=["GET"])
def get_manual_by_id(manual_id):
    """
    Публичный просмотр мануала.

    Гость может смотреть только approved.
    Автор — свой любой статус.
    Админ — любой.
    """
    user_id = _optional_user_id()

    if user_id is None:
        from app.extensions import db
        from app.models.manual import Manual

        manual_record = db.session.get(Manual, manual_id)
        if not manual_record or manual_record.status != "approved":
            from app.exceptions import NotFoundError

            raise NotFoundError("Мануал не найден")
    else:
        manual_record = ManualService.get_manual_for_user(
            manual_id=manual_id,
            user_id=user_id,
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
    ManualService.delete_manual(manual_id=manual_id, user_id=int(get_jwt_identity()))
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
    return (
        jsonify(
            {
                "message": "Изображение загружено",
                "image_url": image_url,
            }
        ),
        200,
    )


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
