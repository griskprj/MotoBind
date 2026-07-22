from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from sqlalchemy import or_

from app.extensions import db
from app.models.user import User
from app.models.motorcycle import Motorcycle
from app.models.maintenance import PlannedMaintenance
from app.models.manual import Manual
from app.exceptions import NotFoundError, ForbiddenError, BusinessLogicError, ValidationError
from app.schemas.manual import CreateMaintenanceSchema, UpdateManualSchema
from app.services.manual_service import ManualService


manual = Blueprint('maunal', __name__)

@manual.route("/", methods=['GET'])
@jwt_required()
def get_maintenance_manual():
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

    maintenance_id = request.args.get('maintenance_id', type=int)
    moto_id = request.args.get('moto_id', type=int)

    if not maintenance_id:
        raise BusinessLogicError("Не указан ID обслуживания")
    if not moto_id:
        raise BusinessLogicError("Не указан ID мотоцикла")

    maintenance = PlannedMaintenance.query.get(maintenance_id)
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
    search_words = re.findall(r'\w+', maintenance_title)
    
    if not search_words:
        raise NotFoundError("Некорректное название обслуживания для поиска мануала")

    conditions = []
    for word in search_words:
        conditions.append(Manual.title.ilike(f'%{word}%'))
    
    manuals_found = Manual.query.filter(
        Manual.motorcycle.ilike(f'%{motorcycle_name}%'),
        *conditions
    ).all()
    
    if not manuals_found:
        manuals_found = Manual.query.filter(
            Manual.motorcycle.ilike(f'%{motorcycle_name}%'),
            or_(*conditions)
        ).all()
    
    if not manuals_found:
        brand = motorcycle_name.split()[0] if motorcycle_name.split() else motorcycle_name
        manuals_found = Manual.query.filter(
            Manual.motorcycle.ilike(f'%{brand}%'),
            or_(*conditions)
        ).all()

    if not manuals_found:
        return jsonify([]), 200

    manual = max(manuals_found, key=lambda m: sum(
        1 for word in search_words if word.lower() in m.title.lower() and m.status == 'approved'
    ))

    result = {
        'id': manual.id,
        'title': manual.title,
        'description': manual.description,
        'category': manual.category,
        'difficult': manual.difficult,
        'instruments': manual.instruments,
        'parts': manual.parts,
        'motorcycle': manual.motorcycle,
        'steps': [
            {
                'order': step.order,
                'title': step.title,
                'text': step.text
            }
            for step in sorted(manual.steps, key=lambda s: s.order)
        ]
    }

    return jsonify(result), 200


@manual.route('/new-manual', methods=['POST'])
@jwt_required()
def create_new_manual():
    """
    Создание нового мануала
    ---
    tags:
      - Manual
    summary: Создание нового мануала
    description: Возвращает созданный мануал
    security:
      - Bearer: []
    
    parameters:
      - name: body
        in: body
        required: true
        schema:
            type: object
            required:
                - title
                - description
                - category
                - difficult
                - instruments
                - parts
                - motorcycle
                - steps:
            schema:
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
    responses:
        201:
            description: Мануал создан
            schema:
                type: object
                properties:
                    id:
                        type: integer
                        example: 123
                    title:
                        type: string
                        example: 123
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

    try:
        data = CreateMaintenanceSchema(**request.get_json())
    except Exception as e:
        raise ValidationError(f"Ошибка валидации: {str(e)}")

    user_id = int(get_jwt_identity())

    steps_data = [step.model_dump() for step in data.steps]

    manual = ManualService.create_manual(
        author_id=user_id,
        title=data.title,
        description=data.description,
        category=data.category,
        difficult=data.difficult,
        instruments=data.instruments,
        parts=data.parts,
        motorcycle=data.motorcycle,
        steps=steps_data
    )

    return jsonify(manual.to_dict()), 201


@manual.route('/<int:manual_id>', methods=['PUT'])
@jwt_required()
def update_manual(manual_id):
    """
    Обновление мануала
    """

    data = UpdateManualSchema(**request.get_json)

    updates = data.get_updates()
    if not updates:
        raise ValidationError("Нет данных для обновления")
    
    user_id = int(get_jwt_identity())

    if 'steps' in updates:
        updates['steps'] = [step.model_dump() for step in updates['steps']]

    manual = ManualService.update_manual(
        manual_id=manual_id,
        user_id=user_id,
        **updates
    )

    return jsonify(manual.to_dict()), 200