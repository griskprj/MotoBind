from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.orm import selectinload
from datetime import datetime, timezone
from app.extensions import db
from app.models.user import User
from app.models.maintenance import Maintenance, PlannedMaintenance
from app.models.motorcycle import Motorcycle
from app.exceptions import BusinessLogicError, ValidationError, ConflictError, NotFoundError, UnauthorizedError, ForbiddenError
from app.schemas.maintenance import CreateMaintenanceSchema, CreatePlannedMaintenanceSchema, UpdatePlannedMaintenanceShema, MarkPlannedMaintenanceSchema
from app.services.maintenance_service import MaintenanceService


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
                category:
                    type: string
                    example: "engine"
                    description: Категория обслуживания
                title:
                    type: string
                    example: Замена масла
                    description: "Название обслуживания"
                description:
                    type: string
                    example: "Замена масла и масляного фильтра"
                    description: Описание (опционально)
                mileage:
                    type: number
                    example: 12790
                    description: "Пробег на момент обслуживания"
                cost:
                    type: number
                    example: 1000
                    description: "Стоимость обслуживания"
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
                    category:
                        type: string
                        example: "engine"
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

    data = CreateMaintenanceSchema(**request.get_json())

    user = User.query.options(
        selectinload(User.motorcycles)
    ).get(get_jwt_identity())

    if not user:
        raise NotFoundError("Пользователь не найден")

    maintenance = MaintenanceService.create_maintenance(
        author_id=int(get_jwt_identity()),
        moto_id=data.id,
        category=data.category,
        title=data.title,
        description=data.description,
        mileage=data.mileage,
        cost=data.cost,
        date=data.date,
    )

    return jsonify(maintenance.to_dict()), 201

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
                - category
            properties:
                moto_id:
                    type: number
                    example: 123
                    description: ID мотоцикла
                title:
                    type: string
                    example: Замена масла
                    description: Название обслуживания
                category:
                    type: string
                    example: Двигатель
                    description: Категория обслуживания
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
                    category:
                        type: string
                        example: "Двигатель"
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
    data = CreatePlannedMaintenanceSchema(**request.get_json())
    
    plan_maintenance = MaintenanceService.create_planned_maintenance(
        author_id=int(get_jwt_identity()),
        moto_id=data.id,
        title=data.title,
        description=data.description,
        category=data.category,
        planned_mileage=data.planned_mileage,
    )

    return jsonify(plan_maintenance.to_dict()), 201


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
    data = UpdatePlannedMaintenanceShema(**request.get_json())

    updates = data.get_updates()
    if not updates:
        raise ValidationError("Нет данных для обновления")

    user_id = int(get_jwt_identity())
    print(user_id)

    plan_maintenance = MaintenanceService.update_planned_maintenance(
        maintenance_id=data.maintenance_id,
        user_id=user_id,
        **updates
    )

    return jsonify(plan_maintenance.to_dict())


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
    user_id = int(get_jwt_identity())

    MaintenanceService.delete_plan_maintenance(maintenance_id, user_id)

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
                    cost:
                        type: integer
                        example: 5000
                        description: Стоимость выполнения обслуживания
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

    data = MarkPlannedMaintenanceSchema(**request.get_json())
    
    current_user_id = int(get_jwt_identity())

    result = MaintenanceService.mark_planned_as_done(
        planned_id=data.planned_id,
        author_id=current_user_id,
        mileage=data.mileage,
        date=data.date,
        cost=data.cost,
        repeat=data.is_repeat,
        interval=data.interval
    )

    return jsonify({
        'message': 'Обслуживание отмечено как выполненное',
        'new_maintenance': result['new_planned']
    }), 201