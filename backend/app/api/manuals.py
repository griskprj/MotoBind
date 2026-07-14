from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import get_jwt_identity, jwt_required
from sqlalchemy import or_

from app.extensions import db
from app.models.user import User
from app.models.motorcycle import Motorcycle
from app.models.maintenance import PlannedMaintenance
from app.models.manual import Manual, ManualStep
from app.exceptions import NotFoundError, ForbiddenError, BusinessLogicError, ValidationError
from app.decorators import admin_required


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
    print(maintenance_id, moto_id)

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
        1 for word in search_words if word.lower() in m.title.lower()
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
@admin_required
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

    data = request.get_json()

    if not data:
        raise ValidationError("Нет данных")
    
    required = ['title', 'category', 'motorcycle']
    for filed in required:
        if filed not in data or not data[filed]:
            raise ValidationError(f"Пропущено обязательное поле {field}")
        
    steps_data = data.get('steps', [])
    if not isinstance(steps_data, list) or len(steps_data) == 0:
        raise ValidationError("В мануале должен быть хотя бы один шаг")

    for idx, step in enumerate(steps_data):
        if 'title' not in step or not step['title']:
            return ValidationError(f"Шаг {idx} не имеет заголовка")
        
        if 'order' not in step:
            step['order'] = idx + 1
    
    db.session.begin()

    manual = Manual(
        title=data['title'],
        description=data.get('description'),
        category=data['category'],
        difficult=data.get('difficult', 'easy'),
        instruments=data.get('instruments'),
        parts=data.get('parts'),
        motorcycle=data['motorcycle']
    )

    for step_data in steps_data:
        if 'order' not in step_data or 'title' not in step_data:
                raise ValidationError("Заполните обязательные поля")

        step = ManualStep(
            order=step_data['order'],
            title=step_data['title'],
            text=step_data['text'] if step_data['text'] else None
        )
        manual.steps.append(step)
    
    try:
        db.session.add(manual)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Failed create manual: {str(e)}')
        raise BusinessLogicError("Ошибка создания мануала")

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
    return jsonify(result), 201
