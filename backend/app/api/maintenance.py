from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.orm import selectinload
from datetime import datetime, timezone
from app.extensions import db
from app.models.user import User
from app.models.maintenance import Maintenance, PlannedMaintenance
from app.models.motorcycle import Motorcycle
from app.exceptions import BusinessLogicError, ValidationError, ConflictError, NotFoundError, UnauthorizedError, ForbiddenError


maintenance = Blueprint('maintenance', __name__)


@maintenance.route('/create-new', methods=['POST'])
@jwt_required()
def create_new_maintenance():
    """
    Создание записи обслуживания
    ---
    tags:
      - Maintenance
    summary: Добавление обслуживания
    description: Создает запись обслуживания
    security:
      - Bearer: []

    parameters:
      - name: body
        in: body
        required: true
        schema:
            type: object
            required:
                - moto_id
                - title
            properties:
                moto_id:
                    type: number
                    example: 123
                    description: ID мотоцикла
                title:
                    type: string
                    example: Замена масла
                    description: Название обслуживания
                description:
                    type: string
                    example: Замена масла и масляного фильтра
                    description: Описание (опционально)
                mileage:
                    type: number
                    example: 12790
                    description: Пробег на момент обслуживания
                date:
                    type: string
                    format: date
                    example: "2026-06-29"
                    description: Дата выполнения (опционально, по умолчанию сегодня)
    resoponses:
        201:
            decsription: Обслуживание создано
            schema:
                type: object
                properties:
                    id:
                        type: integer
                        example: 42
                    title:
                        type: string
                        example: "Замена масла"
                    description:
                        type: string
                        example: "Замена масла и фильтра"
                    mileage:
                        type: integer
                        example: 15000
                    date:
                        type: string
                        format: date-time
                        example: "2026-06-29T10:30:00Z"
                    created_at:
                        type: string
                        format: date-time
                        example: "2026-06-29T10:30:00Z"
                    moto_id:
                        type: integer
                        example: 1
                    author_id:
                        type: integer
                        example: 5
        400:
            description: Ошибка валидации
            schema:
                type: object
                properties:
                    message:
                        type: string
                        example: "Введите название обслуживания"
        401:
            description: Не авторизован
            schema:
                type: object
                properties:
                    message:
                        type: string
                        example: "Отсутствует JWT-токен"
        403:
            description: Доступ запрещен
            schema:
                type: object
                properties:
                    message:
                        type: string
                        example: "Вы можете добавлять обслуживание только для своего мотоцикла"
        404:
            description: Мотоцикл не найден
            schema:
                type: object
                properties:
                    message:
                        type: string
                        example: "Мотоцикл не найден"
    """

    data = request.get_json()
    if not data:
        raise ValidationError("Нет данных в запросе")

    user = User.query.options(
        selectinload(User.motorcycles)
    ).get(get_jwt_identity())

    if not user:
        raise NotFoundError("Пользователь не найден")

    moto_id = data.get('id')
    title = data.get('title')
    description = data.get('description')
    mileage = data.get('mileage')
    date = data.get('date')

    if not title:
        raise ValidationError("Введите название обслуживания")
    if not moto_id:
        raise ValidationError("Отсутсвует ID мотоцикла")

    motorcycle = Motorcycle.query.get(moto_id)
    if not motorcycle:
        raise NotFoundError("Мотоцикл не найден")

    moto_ids = {m.id for m in user.motorcycles}
    if moto_id not in moto_ids:
        raise ForbiddenError("Вы можете добавлять обслуживание только для своего мотоцикла")
    
    try:
        maintenance = Maintenance(
            author_id=user.id,
            moto_id=moto_id,
            title=title,
            description=description,
            mileage=mileage,
            date=datetime.strptime(date, "%Y-%m-%d") if date else None
        )

        db.session.add(maintenance)
        db.session.commit()
        
        return jsonify(maintenance.to_dict()), 201
    except Exception as e:
        current_app.logger.error(f'Failed add maintenance: {str(e)}')
        raise BusinessLogicError("Внутренняя ошибка сервера")


@maintenance.route('/plan', methods=['POST'])
@jwt_required()
def plan_maintenance():
    """
    Планирование обслуживания
    ---
    tags:
      - Maintenance
    summary: Планирование обслуживания
    description: Создает запись запланированного обслуживания
    security:
      - Bearer: []
    parameters:
      - name: body
        in: body
        required: true
        schema:
            type: object
            required:
                - moto_id
                - title
            properties:
                moto_id:
                    type: number
                    example: 123
                    description: ID мотоцикла
                title:
                    type: string
                    example: Замена масла
                    description: Название обслуживания
                description:
                    type: string
                    example: Замена масла и масляного фильтра
                    description: Описание (опционально)
                mileage:
                    type: number
                    example: 12790
                    description: Запланированный пробег обслуживания
    resoponses:
        201:
            decsription: Обслуживание создано
            schema:
                type: object
                properties:
                    id:
                        type: integer
                        example: 42
                    title:
                        type: string
                        example: "Замена масла"
                    description:
                        type: string
                        example: "Замена масла и фильтра"
                    planned_mileage:
                        type: integer
                        example: 15000
                    status:
                        type: string
                        example: "planned"
                    created_at:
                        type: string
                        format: date-time
                        example: "2026-06-29T10:30:00Z"
                    updated_at:
                        type: string
                        format: date-time
                        example: "2026-06-29T10:30:00Z"
                    moto_id:
                        type: integer
                        example: 1
                    author_id:
                        type: integer
                        example: 5
        400:
            description: Ошибка валидации
            schema:
                type: object
                properties:
                    message:
                        type: string
                        example: "Введите название обслуживания"
        401:
            description: Не авторизован
            schema:
                type: object
                properties:
                    message:
                        type: string
                        example: "Отсутствует JWT-токен"
        403:
            description: Доступ запрещен
            schema:
                type: object
                properties:
                    message:
                        type: string
                        example: "Вы можете планировать обслуживание только для своего мотоцикла"
        404:
            description: Мотоцикл не найден
            schema:
                type: object
                properties:
                    message:
                        type: string
                        example: "Мотоцикл не найден"
    """
    data = request.get_json()
    if not data:
        raise ValidationError("Нет данных в запросе")
    
    moto_id = data.get('id')
    title = data.get('title')
    description = data.get('description')
    mileage = data.get('mileage')

    user = User.query.options(
        selectinload(User.motorcycles)
    ).get(get_jwt_identity())

    if not user:
        raise NotFoundError("Пользователь не найден")

    motorcycle = Motorcycle.query.get(moto_id)
    if not motorcycle:
        raise NotFoundError("Мотоцикл не найден")
    
    moto_ids = {m.id for m in user.motorcycles}
    if moto_id not in moto_ids:
        raise ForbiddenError("Вы можете планировать обслуживание только для своего мотоцикла")

    if not title:
        raise ValidationError("Введите заголовок")
    if not moto_id:
        raise ValidationError("Не указан ID мотоцикла")
    
    if mileage and mileage < motorcycle.mileage:
        raise ValidationError("Указан пробег меньше пробега мотоцикла")

    try:
        maintenance = PlannedMaintenance(
            author_id=user.id,
            moto_id=moto_id,
            title=title,
            description=description,
            planned_mileage=mileage,
        )

        db.session.add(maintenance)
        db.session.commit()
        
        return jsonify(maintenance.to_dict()), 201
    except Exception as e:
        current_app.logger.error(f'Failed add maintenance: {str(e)}')
        raise BusinessLogicError("Внутренняя ошибка сервера")


@maintenance.route('/plan', methods=['PUT'])
@jwt_required()
def edit_plan_maintenance():
    """
    Редактирование планового обслуживания
    ---
    tags:
      - Maintenance
    summary: Изменить плановое обслуживание
    description: Редактирует запланированное обслуживание
    security:
      - Bearer: []
    parameters:
      - name: body
        in: body
        required: true
        schema:
            type: object
            required:
                - maintenanceId
            properties:
                maintenanceId:
                    type: number
                    example: 123
                    description: ID обслуживания
                title:
                    type: string
                    example: Замена масла
                    description: Название обслуживания
                description:
                    type: string
                    example: Замена масла и масляного фильтра
                    description: Описание (опционально)
                mileage:
                    type: number
                    example: 12790
                    description: Запланированный пробег обслуживания
    resoponses:
        201:
            decsription: Обновленное плановое обслуживание
            schema:
                type: object
                properties:
                    id:
                        type: integer
                        example: 42
                    title:
                        type: string
                        example: "Замена масла"
                    description:
                        type: string
                        example: "Замена масла и фильтра"
                    planned_mileage:
                        type: integer
                        example: 15000
                    status:
                        type: string
                        example: "planned"
                    created_at:
                        type: string
                        format: date-time
                        example: "2026-06-29T10:30:00Z"
                    updated_at:
                        type: string
                        format: date-time
                        example: "2026-06-29T10:30:00Z"
                    moto_id:
                        type: integer
                        example: 1
                    author_id:
                        type: integer
                        example: 5
        400:
            description: Ошибка валидации
            schema:
                type: object
                properties:
                    message:
                        type: string
                        example: "Введите название обслуживания"
        401:
            description: Не авторизован
            schema:
                type: object
                properties:
                    message:
                        type: string
                        example: "Отсутствует JWT-токен"
        403:
            description: Доступ запрещен
            schema:
                type: object
                properties:
                    message:
                        type: string
                        example: "Вы можете редактировать только свое обслуживание"
        404:
            description: Обслуживание не найдено
            schema:
                type: object
                properties:
                    message:
                        type: string
                        example: "Обслуживание не найдено"
        """
    data = request.get_json()
    if not data:
        raise ValidationError("Нет данных в запросе")

    maintenance_id = data.get('maintenanceId')
    motorcycle_id = data.get('motorcycleId')
    title = data.get('title')
    description = data.get('description')
    mileage = data.get('mileage')

    if not maintenance_id:
        raise ValidationError("Не указан ID обслуживания")

    maintenance = PlannedMaintenance.query.get(maintenance_id)
    if not maintenance:
        raise NotFoundError("Обслуживание не найдено")
    
    if maintenance.author_id != int(get_jwt_identity()):
        raise ForbiddenError("Вы можете редактировать только свое обслуживание")
    
    try:
        if motorcycle_id:
            maintenance.moto_id = motorcycle_id
        if title:
            maintenance.title = title
        if description:
            maintenance.description = description
        if mileage:
            maintenance.planned_mileage = mileage
        db.session.commit()
    
        return jsonify(maintenance.to_dict())
    except Exception as e:
        current_app.logger.error(f'Failed update plan maintenance: {str(e)}')
        raise BusinessLogicError("Ошибка редактирования планового обслуживания")


@maintenance.route('/plan/<int:maintenance_id>', methods=['DELETE'])
@jwt_required()
def delete_plan_maintenance(maintenance_id):
    """
    Удаление планового обслуживания
    ---
    tags:
      - Maintenance
    summary: Удалить плановое обслуживание
    description: Удаление планового обслуживания
    security:
      - Bearer: []
    parameters:
      - name: maintenance_id
        in: path
        required: true
        schema:
            type: integer
        description: ID записи обслуживания
    responses:
        200:
            description: Запись удалена
            schema:
                type: object
                properties:
                    message:
                        type: string
                        example: "Запись удалена"
        403:
            description: Доступ запрещен
            schema:
                type: object
                properties:
                    message:
                        type: string
                        example: "Вы можете удалять только свои записи"
        404:
            description: Запись не найдена
            schema:
                type: object
                properties:
                    message:
                        type: string
                        example: "Запись не найдена"
    """
    maintenance = PlannedMaintenance.query.get(maintenance_id)
    current_user_id = int(get_jwt_identity())

    if not maintenance:
        raise NotFoundError("Запись не найдена")

    if maintenance.author_id != current_user_id and user.role != 'admin':
        raise ForbiddenError("Вы можете удалять только свои записи")
    
    try:
        db.session.delete(maintenance)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(f'Failed delete plan maintenance')
        raise BusinessLogicError("Ошибка удаления планового обслуживания")

    return jsonify({'message': 'Запись удалена'}), 200


@maintenance.route('/plan/mark', methods=['POST'])
@jwt_required()
def mark_maintenance():
    """
    Отметка о выполнении планового обслуживания
    ---
    tags:
        - Maintenance
    summary: Отметить обслуживание как выполненное
    description: |
        Переносит запись из плановых в выполненные.
        Если isRepeat=true — создает новое плановое обслуживание.
    security:
        - Bearer: []
    parameters:
          - name: body
            in: body
            required: true
            schema:
                type: object
                required:
                  - id
                  - mileage
                  - date
                properties:
                    id:
                        type: integer
                        example: 15
                        description: ID планового обслуживания
                    mileage:
                        type: integer
                        example: 18500
                        description: Фактический пробег на момент выполнения
                    date:
                        type: string
                        format: date
                        example: "2026-06-29"
                        description: Дата выполнения
                    isRepeat:
                        type: boolean
                        example: true
                        description: Повторять обслуживание
                    interval:
                        type: integer
                        example: 5000
                        description: Интервал повторения в км (если isRepeat=true)
    responses:
        201:
            description: Обслуживание отмечено
            schema:
                type: object
                properties:
                    message:
                        type: string
                        example: "Обслуживание отмечено"
                    maintenance:
                        type: object
                        description: Новое плановое обслуживание (если isRepeat=true)
                        properties:
                            id:
                                type: integer
                                example: 20
                            title:
                                type: string
                                example: "Замена ремня ГРМ"
                            planned_mileage:
                                type: integer
                                example: 23500
        400:
            description: Ошибка валидации
            schema:
                type: object
                properties:
                    message:
                        type: string
                        example: "Дата не может быть в будущем"
        404:
            description: Обслуживание не найдено
            schema:
                type: object
                properties:
                    message:
                        type: string
                        example: "Обслуживание не найдено"
    """

    data = request.get_json()
    if not data:
        raise ValidationError("Нет данных в запросе")
    
    maintenance_id = data.get('id')
    mileage = data.get('mileage')
    date = data.get('date')
    is_repeat = data.get('isRepeat')
    interval = data.get('interval')
    current_user_id = int(get_jwt_identity())

    if not maintenance_id:
        raise ValidationError("Не указан ID обслуживания")
    if not mileage:
        raise ValidationError("Введите пробег выполнения")
    
    if not date:
        date_obj = datetime.now()
    else:
        try:
            date_obj = datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            raise ValidationError("Неверный формат даты. Используйте ГГГ-ММ-ДД")

    if date_obj > datetime.now():
        raise ValidationError("Дата не может быть в будущем")
    
    if is_repeat and not interval:
        raise ValidationError("Не указан интервал повторения")
    
    try:
        db.session.begin()

        maintenance = PlannedMaintenance.query.get(maintenance_id)
        if not maintenance:
            raise NotFoundError("Обслуживание не найдено")
    
        moto = Motorcycle.query.get(maintenance.moto_id)
        if not moto:
            raise NotFoundError("Мотоцикл не найден")

        new_maintenance = Maintenance(
            moto_id=moto.id,
            author_id=current_user_id,
            title=maintenance.title,
            description=maintenance.description,
            mileage=mileage,
            date=date_obj
        )
        db.session.add(new_maintenance)

        if mileage > moto.mileage:
            moto.mileage = mileage
        
        planned_maintenance = None
        if is_repeat:
            planned_mileage = moto.mileage + interval
            planned_maintenance = PlannedMaintenance(
                author_id=current_user_id,
                moto_id=moto.id,
                title=maintenance.title,
                description=maintenance.description,
                planned_mileage=planned_mileage,
            )
            db.session.add(planned_maintenance)
        
        db.session.delete(maintenance)

        db.session.commit()

        return jsonify({ 
            'maintenance': planned_maintenance.to_dict()  if planned_maintenance else None,
            'message': 'Обслуживание отмечено'}
        ), 201
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Failed mark maintenance: {str(e)}')
        raise BusinessLogicError("Внутренняя ошибка сервера")