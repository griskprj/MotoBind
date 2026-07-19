from flask import Blueprint, jsonify, request, current_app, send_from_directory
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime, timezone
from app.extensions import db
from app.models.user import User
from app.models.motorcycle import Motorcycle
from app.models.maintenance_node import MaintenanceNode
from app.utils.files import allowed_file, save_moto_photo
from app.exceptions import BusinessLogicError, ValidationError, ConflictError, NotFoundError, UnauthorizedError, ForbiddenError
from app.schemas.motorcycle import CreateMotorcycleSchema, UpdateMotorcycleSchema
from app.services.motorcycle_service import MotorcycleService


motorcycle = Blueprint('motorcycle', __name__)


@motorcycle.route('/my', methods=['GET'])
@jwt_required()
def get_user_moto():
    """
    Получение данных о мотоциклах пользователя.
    ---
    tags:
      - Motorcycle
    summary: Получение данных о мотоциклах пользователя
    description: Получение данных о мотоциклах пользователя по его идентификатору.
    security:
        - Bearer: []
    responses:
        200:
            description: Успешный ответ с данными о мотоциклах пользователя
            schema:
                type: array
                items:
                    type: object
                    properties:
                        id:
                            type: integer
                            description: Идентификатор мотоцикла
                        name:
                            type: string
                            description: Название мотоцикла
                        years:
                            type: integer
                            description: Год выпуска мотоцикла
                        volume:
                            type: integer
                            description: Объем двигателя мотоцикла
                        mileage:
                            type: integer
                            description: Пробег мотоцикла
                        color:
                            type: string
                            description: Цвет мотоцикла
                        license_plate:
                            type: string
                            description: Государственный номер мотоцикла
                        vin:
                            type: string
                            description: VIN мотоцикла
        404:
            description: Пользователь не найден
        500:
            description: Ошибка сервера
    """
    current_user_id = int(get_jwt_identity())

    user = User.query.get(current_user_id)
    if not user:
                raise NotFoundError('Пользователь не найден')
    
    motorcycles = MotorcycleService.get_motorcycle_by_id(current_user_id)
    return jsonify([m.to_dict() for m in motorcycles]), 200



@motorcycle.route('/new', methods=['POST'])
@jwt_required()
def create_moto():
    """
    Создать новый мотоцикл для пользователя.
    ---
    tags:
        - Motorcycle
    summary: Создание нового мотоцикла
    description: Создание нового мотоцикла для пользователя с указанием необходимых данных. Автоматически создает узлы обслуживания
    security:
        - Bearer: []
    parameters:
        - in: body
          name: body
          required: true
          schema:
            type: object
            properties:
                name:
                    type: string
                    description: Название мотоцикла
                years:
                    type: integer
                    description: Год выпуска мотоцикла
                volume:
                    type: integer
                    description: Объем двигателя мотоцикла
                mileage:
                    type: integer
                    description: Пробег мотоцикла
                color:
                    type: string
                    description: Цвет мотоцикла (формат HEX, например, #FFFFFF)
                license_plate:
                    type: string
                    description: Государственный номер мотоцикла
                vin:
                    type: string
                    description: VIN мотоцикла
    responses:
        201:
            description: Мотоцикл успешно создан
            schema:
                type: object
                properties:
                    id:
                        type: integer
                        description: Идентификатор мотоцикла
                    name:
                        type: string
                        description: Название мотоцикла
                    years:
                        type: integer
                        description: Год выпуска мотоцикла
                    volume:
                        type: integer
                        description: Объем двигателя мотоцикла
                    mileage:
                        type: integer
                        description: Пробег мотоцикла
                    color:
                        type: string
                        description: Цвет мотоцикла
                    license_plate:
                        type: string
                        description: Государственный номер мотоцикла
                    vin:
                        type: string
                        description: VIN мотоцикла
        400:
            description: Ошибка валидации данных
        500:
            description: Ошибка сервера
    """
    data = CreateMotorcycleSchema(**request.get_json())

    moto = MotorcycleService.create_motorcycle(
        owner_id=int(get_jwt_identity()),
        name=data.name,
        years=data.years,
        volume=data.volume,
        mileage=data.mileage,
        color=data.color,
        license_plate=data.license_plate,
        vin=data.vin
    )

    return jsonify(moto.to_dict()), 201


@motorcycle.route('/<int:moto_id>', methods=['PUT'])
@jwt_required()
def update_moto(moto_id):
    """
    Обновление данных мотоцикла.
    ---
    tags:
      - Motorcycle
    summary: Обновление данных мотоцикла
    description: Обновление данных мотоцикла по его идентификатору.
    security:
        - Bearer: []
    parameters:
          - in: path
            name: moto_id
            required: true
            type: integer
            description: Идентификатор мотоцикла
          - in: body
            name: body
            required: true
            schema:
                type: object
                properties:
                    name:
                        type: string
                        description: Название мотоцикла
                    years:
                        type: integer
                        description: Год выпуска мотоцикла
                    volume:
                        type: integer
                        description: Объем двигателя мотоцикла
                    mileage:
                        type: integer
                        description: Пробег мотоцикла
                    color:
                        type: string
                        description: Цвет мотоцикла (формат HEX, например, #FFFFFF)
                    license_plate:
                        type: string
                        description: Государственный номер мотоцикла
                    vin:
                        type: string
                        description: VIN мотоцикла
    responses:
        200:
            description: Данные мотоцикла успешно обновлены
            schema:
                type: object
                properties:
                    id:
                        type: integer
                        description: Идентификатор мотоцикла
                    name:
                        type: string
                        description: Название мотоцикла
                    years:
                        type: integer
                        description: Год выпуска мотоцикла
                    volume:
                        type: integer
                        description: Объем двигателя мотоцикла
                    mileage:
                        type: integer
                        description: Пробег мотоцикла
                    color:
                        type: string
                        description: Цвет мотоцикла
                    license_plate:
                        type: string
                        description: Государственный номер мотоцикла
                    vin:
                        type: string
                        description: VIN мотоцикла
                    
        400:
            description: Ошибка валидации данных
        404:
            description: Мотоцикл не найден
        500:
            description: Ошибка сервера
    """
    data = UpdateMotorcycleSchema(**request.get_json())
    user_id = int(get_jwt_identity())
    
    motorcycle = MotorcycleService.update_motorcycle(
        moto_id=moto_id,
        user_id=user_id,
        name=data.name,
        years=data.years,
        volume=data.volume,
        mileage=data.mileage,
        color=data.color,
        license_plate=data.license_plate,
        vin=data.vin
    )

    return jsonify(motorcycle.to_dict()), 200

@motorcycle.route('/<int:moto_id>', methods=['PATCH'])
@jwt_required()
def update_moto_mileage(moto_id):
    """
    Обновить пробег мотоцикла.
    ---
    tags:
        - Motorcycle
    summary: Обновление пробега мотоцикла
    description: Обновление пробега мотоцикла по его идентификатору.
    security:
        - Bearer: []
    parameters:
        - in: path
          name: moto_id
          required: true
          type: integer
          description: Идентификатор мотоцикла
        - in: body
          name: body
          required: true
          schema:
              type: object
              properties:
                  newMileage:
                      type: integer
                      description: Новый пробег мотоцикла
    responses:
        200:
            description: Пробег мотоцикла успешно обновлен
            schema:
                type: object
                properties:
                    id:
                        type: integer
                        description: Идентификатор мотоцикла
                    name:
                        type: string
                        description: Название мотоцикла
                    years:
                        type: integer
                        description: Год выпуска мотоцикла
                    volume:
                        type: integer
                        description: Объем двигателя мотоцикла
                    mileage:
                        type: integer
                        description: Пробег мотоцикла
        400:
            description: Ошибка валидации данных
        404:
            description: Мотоцикл не найден
        500:
            description: Ошибка сервера
    """
    data = request.get_json()
    if not data:
        raise ValidationError('Нет данных для обновления')
    
    new_mileage = data.get('newMileage')
    if new_mileage is None:
        raise ValidationError('Укажите новый пробег')
    
    if not isinstance(new_mileage, int) or new_mileage < 0:
        raise ValidationError('Пробег должен быть положительным числом')
    
    user_id = int(get_jwt_identity())
    
    moto = MotorcycleService.update_motorcycle(
        moto_id=moto_id,
        user_id=user_id,
        mileage=new_mileage
    )
    
    return jsonify(moto.to_dict()), 200


@motorcycle.route('/<int:moto_id>', methods=['DELETE'])
@jwt_required()
def delete_moto(moto_id):
    """
    Удаление мотоцикла по его идентификатору.
    ---
    tags:
      - Motorcycle
    summary: Удаление мотоцикла
    description: Удаление мотоцикла по его идентификатору.
    security:
        - Bearer: []
    parameters:
        - in: path
          name: moto_id
          required: true
          type: integer
          description: Идентификатор мотоцикла
    responses:
        200:
            description: Мотоцикл успешно удален
            schema:
                type: object
                properties:
                    message:
                        type: string
                        description: Сообщение об успешном удалении мотоцикла
        404:
            description: Мотоцикл не найден
        500:
            description: Ошибка сервера
    """
    user_id = int(get_jwt_identity())

    MotorcycleService.delete_motorcycle(moto_id, user_id)

    return jsonify({'message': 'Мотоцикл удален'}), 200