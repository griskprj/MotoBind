from flask import Blueprint, jsonify, request, current_app
from flask_jwt_extended import get_jwt_identity, jwt_required
import json

from app.exceptions import ForbiddenError, NotFoundError, ValidationError
from app.extensions import db
from app.models.manual import Manual
from app.models.user import User
from app.schemas.manual import CreateManualSchema, UpdateManualSchema
from app.services.manual_service import ManualService

manual = Blueprint("manual", __name__)


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
    return jsonify(data), 200


@manual.route("/<int:manual_id>", methods=["GET"])
@jwt_required()
def get_manual_by_id(manual_id):
    """Получение детальной информации о мануале."""
    manual_record = ManualService.get_manual_for_user(
        manual_id=manual_id,
        user_id=int(get_jwt_identity()),
    )
    return jsonify(manual_record.to_dict()), 200


@manual.route("/new-manual", methods=["POST"])
@jwt_required()
def create_manual():
    """
    Создание мануала с файлами
    """
    try:
        data = request.form.get('data')
        if not data:
            raise ValidationError("Данные не переданы")
        
        data = json.loads(data)
        
        files = request.files.to_dict() if request.files else {}
        
        schema = CreateManualSchema(**data)
        
        manual = ManualService.create_manual(
            author_id=int(get_jwt_identity()),
            data=schema.model_dump(),
            files=files
        )

        return jsonify(manual.to_dict()), 201
        
    except json.JSONDecodeError:
        raise ValidationError("Неверный формат JSON")
    except Exception as e:
        current_app.logger.error(f"Ошибка создания мануала: {e}")
        raise


@manual.route("/<int:manual_id>", methods=["PUT"])
@jwt_required()
def update_manual(manual_id):
    """
    Обновление мануала
    """
    user_id = int(get_jwt_identity())
    user = db.session.get(User, user_id)
    is_admin = user.role == 'admin' if user else False

    data = UpdateManualSchema(**request.get_json())

    manual = ManualService.update_manual(
        manual_id=manual_id,
        user_id=user_id,
        is_admin=is_admin,
        **data.get_updates()
    )
    return jsonify(manual.to_dict()), 200


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
    """
    Загрузка изображения для шага мануала
    """
    from app.utils.files import save_step_image
    
    manual = db.session.get(Manual, manual_id)
    if not manual:
        raise NotFoundError("Мануал не найден")
    
    current_user_id = int(get_jwt_identity())
    if manual.author_id != current_user_id:
        raise ForbiddenError("Вы можете редактировать только свои мануалы")
    
    step = None
    for s in manual.steps:
        if s.id == step_id:
            step = s
            break
    
    if not step:
        raise NotFoundError("Шаг не найден")
    
    if 'image' not in request.files:
        raise ValidationError("Файл изображения не найден")
    
    file = request.files['image']
    if not file or file.filename == '':
        raise ValidationError("Файл не выбран")
    
    image_url = save_step_image(file, manual_id, step_id)
    
    step.image = image_url
    db.session.commit()
    
    return jsonify({
        "message": "Изображение загружено",
        "image_url": image_url
    }), 200


@manual.route("/<int:manual_id>/steps/<int:step_id>/image", methods=["DELETE"])
@jwt_required()
def delete_step_image(manual_id, step_id):
    """
    Удаление изображения шага
    """
    from app.utils.files import delete_file
    
    manual = db.session.get(Manual, manual_id)
    if not manual:
        raise NotFoundError("Мануал не найден")
    
    current_user_id = int(get_jwt_identity())
    if manual.author_id != current_user_id:
        raise ForbiddenError("Вы можете редактировать только свои мануалы")
    
    step = None
    for s in manual.steps:
        if s.id == step_id:
            step = s
            break
    
    if not step:
        raise NotFoundError("Шаг не найден")
    
    if step.image:
        delete_file(step.image)
        step.image = None
        db.session.commit()
    
    return jsonify({"message": "Изображение удалено"}), 200