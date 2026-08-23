from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from sqlalchemy import or_

from app.exceptions import ForbiddenError, NotFoundError
from app.models.maintenance import Maintenance
from app.models.manual import Manual
from app.models.motorcycle import Motorcycle
from app.models.user import User
from app.schemas.manual import CreateManualSchema
from app.services.manual_service import ManualService

manual = Blueprint("maunal", __name__)


@manual.route("/", methods=["GET"])
@jwt_required()
def get_manual_for_maintenance():
    """
    Получение мануала для конкретного обслуживания
    ---
    tags:
      - Manual
    summary: Получение мануала для конкретного обслуживания
    description: Возвращает мануал для конкретного мотоцикла и обслуживания
    security:
      - Bearer: []

    parameters:
      - name: maintenance_id
        in: query
        required: true
        type: integer
        description: ID планового обслуживания
      - name: moto_id
        in: query
        required: true
        type: integer
        description: ID мотоцикла

    responses:
        200:
            description: Мануал получен
            schema:
                type: object
                properties:
                    id:
                        type: integer
                        example: 123
                    title:
                        type: string
                        example: "Замена масла"
                    description:
                        type: string
                        example: "Инструкция по замене масла"
                    category:
                        type: string
                        example: "Двигатель"
                    difficult:
                        type: string
                        example: "Легко"
                    instruments:
                        type: string
                        example: "Ключ на 18мм, ветошь"
                    parts:
                        type: string
                        example: "Масло, фильтр"
                    motorcycle:
                        type: string
                        example: "BMW S1000RR"
                    steps:
                        type: array
                        items:
                            type: object
                            properties:
                                order:
                                    type: integer
                                title:
                                    type: string
                                text:
                                    type: string
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

    maintenance_title = maintenance.title.lower()
    motorcycle_name = motorcycle.name.lower()

    import re

    search_words = re.findall(r"\w+", maintenance_title)

    if not search_words:
        raise NotFoundError("Некорректное название обслуживания для поиска мануала")

    conditions = []
    for word in search_words:
        conditions.append(Manual.title.ilike(f"%{word}%"))

    manuals_found = Manual.query.filter(
        Manual.motorcycle.ilike(f"%{motorcycle_name}%"), *conditions
    ).all()

    if not manuals_found:
        manuals_found = Manual.query.filter(
            Manual.motorcycle.ilike(f"%{motorcycle_name}%"), or_(*conditions)
        ).all()

    if not manuals_found:
        brand = (
            motorcycle_name.split()[0] if motorcycle_name.split() else motorcycle_name
        )
        manuals_found = Manual.query.filter(
            Manual.motorcycle.ilike(f"%{brand}%"), or_(*conditions)
        ).all()

    if not manuals_found:
        return jsonify([]), 200

    manual = max(
        manuals_found,
        key=lambda m: sum(
            1
            for word in search_words
            if word.lower() in m.title.lower() and m.status == "approved"
        ),
    )

    result = {
        "id": manual.id,
        "title": manual.title,
        "description": manual.description[:200],
        "category": manual.category,
        "difficult": manual.difficult,
        "instruments": manual.instruments or "",
        "parts": manual.parts or "",
        "motorcycle": manual.motorcycle,
        "tip": manual.tip or "",
        "steps": [
            {"order": step.order, "title": step.title, "text": step.text, "tip": step.tip, "warning": step.warning}
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
    sort_by = request.args.get("sort_by", "created_at_dec")

    query = Manual.query

    if tab == "my":
        query = query.filter(Manual.author_id == current_user_id)
    elif tab == "myMotos":
        user_motorcycles = Motorcycle.query.filter_by(owner_id=current_user_id).all()

        moto_names = [moto.name for moto in user_motorcycles]
        if moto_names:
            query = query.filter(Manual.motorcycle.in_(moto_names))
        else:
            return (
                jsonify(
                    {
                        "manuals": [],
                        "total": 0,
                        "pages": 0,
                        "current_page": page,
                        "per_page": per_page,
                        "has_prev": False,
                        "has_next": False,
                    }
                ),
                200,
            )

    if search:
        query = query.filter(
            or_(
                Manual.title.ilike(f"%{search}"),
                Manual.motorcycle.ilike(f"%{search}"),
                Manual.description.ilike(f"${search}"),
            )
        )

    if motorcycle_filter:
        query = query.filter(Manual.motorcycle.ilike(f"${motorcycle_filter}"))

    if category:
        query = query.filter(Manual.category == category)

    sort_mapping = {
        "created_at_desc": Manual.created_at.desc(),
        "created_at_asc": Manual.created_at.asc(),
        "title_asc": Manual.title.asc(),
        "title_desc": Manual.title.desc(),
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
        raise ForbiddenError("Мануал не был допущен к публикации")

    return jsonify(manual.to_dict())


@manual.route("/new-manual", methods=["POST"])
@jwt_required()
def create_manual():
    """
    Создание мануала
    """
    data = CreateManualSchema(**request.get_json())
    manual = ManualService.create_manual(
        author_id=int(get_jwt_identity()), **data.model_dump()
    )
    return jsonify(manual.to_dict()), 201
