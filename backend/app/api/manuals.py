from flask import Blueprint, jsonify, request, current_app
from flask_jwt_extended import get_jwt_identity, jwt_required
from sqlalchemy import or_

from app.exceptions import ForbiddenError, NotFoundError, ValidationError
from app.extensions import db
from app.models.maintenance import Maintenance
from app.models.manual import Manual
from app.models.motorcycle import Motorcycle
from app.models.user import User
from app.schemas.manual import CreateManualSchema, UpdateManualSchema
from app.services.manual_service import ManualService

manual = Blueprint("manual", __name__)


@manual.route("/", methods=["GET"])
@jwt_required()
def get_manual_for_maintenance():
    """
    Получение мануала для конкретного обслуживания
    """
    maintenance_id = request.args.get("maintenance_id", type=int)
    moto_id = request.args.get("moto_id", type=int)

    maintenance = Maintenance.query.get(maintenance_id)
    motorcycle = Motorcycle.query.get(moto_id)
    user = User.query.get(get_jwt_identity())

    if not maintenance:
        raise NotFoundError("Обслуживание не найдено")
    if not motorcycle:
        raise NotFoundError("Мотоцикл не найден")
    if not user:
        raise NotFoundError("Пользователь не найден")

    if int(maintenance.author_id) != int(user.id):
        raise ForbiddenError("Вы можете выполнять только свое обслуживание")
    if int(motorcycle.owner_id) != int(user.id):
        raise ForbiddenError("Вы не являетесь владельцем этого мотоцикла")

    manual = ManualService.get_manual_for_maintenance(
        maintenance_title=maintenance.title,
        motorcycle_name=motorcycle.name,
        user_id=user.id
    )

    if not manual:
        return jsonify([]), 200

    result = {
        "id": manual.id,
        "title": manual.title,
        "description": manual.description[:200] if manual.description else "",
        "category": manual.category,
        "difficult": manual.difficult,
        "time_estimate": manual.time_estimate,
        "interval": manual.interval,
        "safety_tip": manual.safety_tip,
        "warnings": manual.warnings,
        "conditions": manual.conditions,
        "docs_links": manual.docs_links,
        "specs": manual.specs,
        "aftercare": manual.aftercare,
        "instruments": manual.instruments or "",
        "parts": manual.parts or "",
        "motorcycle": manual.motorcycle,
        "tip": manual.tip or "",
        "steps": [
            {
                "order": step.order,
                "title": step.title or "",
                "text": step.text or "",
                "tip": step.tip or "",
                "warning": step.warning or "",
                "image": step.image or "",
                "result": step.result or ""
            }
            for step in sorted(manual.steps, key=lambda s: s.order)
        ],
    }

    return jsonify(result), 200


@manual.route("/list", methods=["GET"])
@jwt_required()
def list_manuals():
    """
    Получение списка мануалов с пагинацией и фильтрами
    """
    current_user_id = int(get_jwt_identity())

    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 8, type=int)
    tab = request.args.get("tab", "all")
    search = request.args.get("search", "")
    motorcycle_filter = request.args.get("motorcycle", "")
    category = request.args.get("category", "")
    sort_by = request.args.get("sort_by", "created_at_desc")
    difficult = request.args.get("difficult", "")
    time_estimate = request.args.get("time_estimate", "")
    interval = request.args.get("interval", "")
    status = request.args.get("status", "")

    query = Manual.query

    if tab == "my":
        query = query.filter(Manual.author_id == current_user_id)
    elif tab == "myMotos":
        user_motorcycles = Motorcycle.query.filter_by(owner_id=current_user_id).all()
        moto_names = [moto.name for moto in user_motorcycles]
        if moto_names:
            query = query.filter(Manual.motorcycle.in_(moto_names))
        else:
            return jsonify({
                "manuals": [],
                "total": 0,
                "pages": 0,
                "current_page": page,
                "per_page": per_page,
                "has_prev": False,
                "has_next": False,
            }), 200

    if search:
        query = query.filter(
            or_(
                Manual.title.ilike(f"%{search}%"),
                Manual.motorcycle.ilike(f"%{search}%"),
                Manual.description.ilike(f"%{search}%"),
                Manual.author.has(User.username.ilike(f"%{search}%"))
            )
        )

    if motorcycle_filter:
        query = query.filter(Manual.motorcycle.ilike(f"%{motorcycle_filter}%"))

    if category:
        query = query.filter(Manual.category == category)
    
    if difficult:
        query = query.filter(Manual.difficult == difficult)
    
    if time_estimate:
        query = query.filter(Manual.time_estimate.ilike(f"%{time_estimate}%"))
    
    if interval:
        query = query.filter(Manual.interval.ilike(f"%{interval}%"))
    
    if status and (User.query.get(current_user_id)).role == 'admin':
        query = query.filter(Manual.status == status)

    sort_mapping = {
        "created_at_desc": Manual.created_at.desc(),
        "created_at_asc": Manual.created_at.asc(),
        "title_asc": Manual.title.asc(),
        "title_desc": Manual.title.desc(),
        "difficult_asc": Manual.difficult.asc(),
        "difficult_desc": Manual.difficult.desc(),
    }
    query = query.order_by(sort_mapping.get(sort_by, Manual.created_at.desc()))

    paginated = query.paginate(page=page, per_page=per_page, error_out=False)

    result = {
        "manuals": [manual.to_dict() for manual in paginated.items],
        "total": paginated.total,
        "pages": paginated.pages,
        "current_page": paginated.page,
        "per_page": paginated.per_page,
        "has_prev": paginated.has_prev,
        "has_next": paginated.has_next,
    }

    return jsonify(result), 200


@manual.route("/<int:manual_id>", methods=["GET"])
@jwt_required()
def get_manual_by_id(manual_id):
    """
    Получение детальной информации о мануале
    """
    manual = Manual.query.get(manual_id)
    if not manual:
        raise NotFoundError("Мануал не найден")

    if manual.status != "approved":
        current_user_id = int(get_jwt_identity())
        is_admin = current_user_id == 1
        is_author = manual.author_id == current_user_id
        
        if not is_admin and not is_author:
            raise ForbiddenError("Мануал не был допущен к публикации")

    return jsonify(manual.to_dict()), 200


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
        
        import json
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
    user = User.query.get(user_id)
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
    
    manual = Manual.query.get(manual_id)
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
    
    manual = Manual.query.get(manual_id)
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