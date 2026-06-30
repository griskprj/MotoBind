from flask import Blueprint, jsonify, request, current_app, send_from_directory
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime, timezone
from app.extensions import db
from app.models.user import User
from app.models.motorcycle import Motorcycle
from app.utils.files import allowed_file, save_moto_photo
from app.exceptions import BusinessLogicError, ValidationError, ConflictError, NotFoundError, UnauthorizedError, ForbiddenError


motorcycle = Blueprint('motorcycle', __name__)


@motorcycle.route('/my', methods=['GET'])
@jwt_required()
def get_user_moto():
    """
    Получение данных о мотоциклах пользователя.
    ---
    tags
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

    try:
        user = User.query.get(current_user_id)
        if not user:
            raise NotFoundError('Пользователь не найден')
        
        motorcycles = [m.to_dict() for m in user.motorcycles]
        return jsonify(motorcycles), 200

    except Exception as e:
        current_app.logger.error(f'Get motorcycle failed: {str(e)}')
        raise BusinessLogicError('Ошибка при получении данных о мотоциклах пользователя')



@motorcycle.route('/new', methods=['POST'])
@jwt_required()
def create_moto():
    """
    Создать новый мотоцикл для пользователя.
    ---
    tags:
        - Motorcycle
    summary: Создание нового мотоцикла
    description: Создание нового мотоцикла для пользователя с указанием необходимых данных.
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
    data = request.get_json()

    name = data.get('name')
    years = data.get('years')
    volume = data.get('volume')
    mileage = data.get('mileage')
    color = data.get('color')
    license_plate = data.get('license_plate')
    vin = data.get('vin')

    if not name:
        raise ValidationError('Укажите название мотоцикла')
    
    if color and color[0] != '#' and len(color.split('#')[1]) < 3:
        raise ValidationError('Цвет должен быть формата HEX (#FFFFFF)')

    if license_plate and license_plate and len(license_plate) > 9:
        raise ValidationError('Неверный формат ГОС номера')

    if vin and len(vin) != 17:
        raise ValidationError('VIN должен содержать 17 символов')

    if mileage > 1_000_000:
        raise ValidationError('Введите корректный пробег')

    try:
        motorcycle = Motorcycle(
            owner_id=get_jwt_identity(),
            name=name,
            years=years,
            volume=volume,
            mileage=mileage,
            color=color,
            license_plate=license_plate,
            vin=vin
        )
        db.session.add(motorcycle)
        db.session.commit()

        return jsonify(motorcycle.to_dict()), 201
    except Exception as e:
        current_app.logger.error(f'Failed create moto: {str(e)}')
        raise BusinessLogicError("Ошибка создания мотоцикла")


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
    
    motorcycle = Motorcycle.query.get(moto_id)
    if not motorcycle:
        raise NotFoundError('Мотоцикл не найден')

    now = datetime
    try:
        name = data.get('name')
        volume = data.get('volume')
        mileage = data.get('mileage')
        years = data.get('years')
        if 'name' in data:
            motorcycle.name = name
        if 'years' in data and datetime.now().year > years:
            motorcycle.years = years
        if 'volume' in data and 49 <= volume <= 4000:
            motorcycle.volume = volume
        if 'mileage' in data and mileage < 1_000_000:
            motorcycle.mileage = mileage
        
        db.session.commit()
        return jsonify(motorcycle.to_dict())

    except Exception as e:
        current_app.logger.error(f'Failed update moto: {str(e)}')
        raise InternalServerError('Ошибка сервера')



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
    
    motorcycle = Motorcycle.query.get(moto_id)
    if not motorcycle:
        raise NotFoundError('Мотоцикл не найден')

    new_mileage = data.get('newMileage')
    if not new_mileage:
        raise ValidationError('Укажите новый пробег')

    try:
        motorcycle.mileage = int(new_mileage)
        db.session.commit()
        return jsonify(motorcycle.to_dict()), 200

    except ValueError:
        raise ValidationError('Неверный формат пробега')
    except Exception as e:
        current_app.logger.error(f'Failed update moto mileage: {str(e)}')
        raise BusinessLogicError('Ошибка сервера')



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
    motorcycle = Motorcycle.query.get(moto_id)
    if not motorcycle:
        raise NotFoundError('Мотоцикл не найден')
    
    try:
        db.session.delete(motorcycle)
        db.session.commit()
        return jsonify({'message': 'Мотоцикл удален'}), 200
    except Exception as e:
        current_app.logger.error(f'Failed delete moto {str(e)}')
        raise BusinessLogicError('Ошибка сервера')