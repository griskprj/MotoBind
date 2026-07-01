from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import (
    create_access_token, create_refresh_token,
    jwt_required, get_jwt_identity
)
from app.models.user import User
from app.extensions import db
from app.exceptions import BusinessLogicError, ValidationError, ConflictError, NotFoundError, UnauthorizedError, ForbiddenError


auth = Blueprint('auth', __name__)


@auth.route('/register', methods=['POST'])
def register():
    """
    Регистрация нового пользователя
    ---
    tags:
        - Authentication
    summary: Регистрация
    description: Создает нового пользователя
    parameters:
      - name: body
        in: body
        required: true
        schema:
            type: object
            required:
                - email
                - password
                - username
                - role
            properties:
                email:
                    type: string
                    format: email
                    example: user@example.com
                password:
                    type: string
                    minLength: 6
                    example: 123456
                    writeOnly: true
                username:
                    type: string
                    example: MotoBat
                role:
                    type: string
                    example: motorcyclist
                    enum: ['motorcyclist', 'motoclub']
    responses:
        201:
            description: Пользователь создан
            schema:
                type: object
                properties:
                    message:
                        type: string
                        example: "Регистрация успешна"
                    user:
                        type: object
                        properties:
                            id:
                                type: integer
                                example: 123
                            email:
                                type: string
                                example: user@example.com
                            username:
                                type: string
                                example: MotoBat
                            role:
                                type: string
                                example: motorcyclist
                            refresh_token:
                                type: string
                                example: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
        400:
            description: Ошибка валидации
            schema:
                type: object
                properties:
                    message:
                        type: string
                        example: "Ошибка валидации"
                    errors:
                        type: object
                        additionalProperties:
                            type: string
                    example:
                        email: "Пользователь с таким email уже существует"
                        password: "Длина пароля не менее 6 символов"
        409:
            description: Конфликт имен (email или имя пользователя уже зарегистрированы)
            schema:
                type: object
                properties:
                    message:
                        type: string
                        example: "Конфликт имен"
                    error:
                        type: string
                        example: "Пользователь с таким email уже зарегистрирован"
    """

    data = request.get_json()
    if not data:
        raise ValidationError("Нет данных в запросе")

    email = data.get('email')
    password = data.get('password')
    username = data.get('username')
    role = data.get('role')

    if not email:
        raise ValidationError("Введите почту", errors={"email": "Поле email обязательно"})
    if not password:
        raise ValidationError("Введите пароль", errors={"password": "Поле пароля обязательно"})
    if not username:
        raise ValidationError("Введите имя пользователя", errors={"username": "Поле имя пользователя обязательно"})
    if not role:
        raise ValidationError("Выберите роль", errors={"role": "Выбор роли обязателен"})
    
    
    if len(password) < 6:
        raise ValidationError("Длина пароля не менее 6 символов")

    if User.query.filter_by(email=email).first():
        raise ConflictError("Пользователь с таким email уже существует")

    if User.query.filter_by(username=username).first():
        raise ConflictError("Имя пользователя занято")

    try:
        user = User(
            email=email,
            username=username,
            role=role
        )
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        return jsonify({
            'message': 'Регистрация успешна',
            'user': user.to_dict()
        }), 201
    except Exception as e:
        current_app.logger.error(f'Registration failed: {str(e)}')
        raise BusinessLogicError("Ошибка при создании пользователя")


@auth.route('/login', methods=['POST'])
def login():
    """
    Логин пользователя
    ---
    tags:
        - Authentication
    summary: Логин
    description: Авторизует пользователя, выдает acces и refresh токены
    parameters:
      - name: body
        in: body
        required: true
        schema:
            type: object
            required:
                - email
                - password
            properties:
                email:
                    type: string
                    format: email
                    example: user@example.com
                password:
                    type: string
                    example: 123456
                    writeOnly: true
    responses:
        200:
            description: Пользователь авторизован
            schema:
                type: object
                properties:
                    message:
                        type: string
                        example: Вы вошли в аккаунт
                    access_token:
                        type: string
                        example: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
                    refresh_token:
                        type: string
                        example: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
                    user:
                        type: object
                        properties:
                            id:
                                type: integer
                                example: 123
                            email:
                                type: string
                                example: user@example.com
                            username:
                                type: string
                                example: MotoBat
                            role:
                                type: string
                                example: motorcyclist
                            refresh_token:
                                type: string
                                example: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
        400:
            description: Ошибка валидации
            schema:
                type: object
                properties:
                    message:
                        type: string
                        example: "Ошибка валидации"
                    errors:
                        type: object
                        additionalProperties:
                            type: string
                    example:
                        email: "Введите почту"
                        password: "Введите пароль"
                        no_data: "Нет данных"
        401:
            description: Ошибка доступа
            schema:
                type: object
                properties:
                    message:
                        type: string
                        example: "Ошибка доступа"
                    error:
                        type: string
                        example: "Неправильный пароль"
        404:
            description: Объект не найден или не существует
            schema:
                type: object
                properties:
                    message:
                        type: string
                        example: "Объект не найден или не существует"
                    error:
                        type: string
                        example: "Пользователь не найден"
    """

    data = request.get_json()
    if not data:
        raise ValidationError("Нет даных в запросе")
    
    email = data.get('email')
    password = data.get('password')

    if not email:
        raise ValidationError("Введите почту", errors={"email": "Поле email обязательно"})
    if not password:
        raise ValidationError("Введите пароль", errors={"password": "Поле пароля обязательно"})

    user = User.query.filter_by(email=email).first()
    if not user:
        raise NotFoundError("Пользователь с такой почтой не найден")
    if not user.check_password(password):
        raise ForbiddenError("Неверный пароль")
    
    access_token = create_access_token(identity=str(user.id), additional_claims={'role': user.role})
    refresh_token = create_refresh_token(identity=str(user.id))

    user.refresh_token = refresh_token
    db.session.commit()

    return jsonify({
        'message': 'Вы вошли в аккаунт',
        'access_token': access_token,
        'refresh_token': refresh_token,
        'user': user.to_dict()
    }), 200


@auth.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """
    Получение данных текущего пользователя
    ---
    tags:
        - Authentication
    summary: Получить профиль
    description: Возвращает данные авторизованного пользователя
    security:
      - Bearer: []
    responses:
        200:
            description: Успешный ответ
            schema:
                type: object
                properties:
                        id:
                            type: integer
                            example: 123
                        email:
                            type: string
                            example: user@example.com
                        username:
                            type: string
                            example: MotoBat
                        role:
                            type: string
                            example: motorcyclist
        401:
            description: Пользователь не авторизован (отсутсвует или невалидный токен)
            schema:
                type: object
                properties:
                    message:
                        type: string
                        example: "Ошибка доступа"
                    error:
                        type: string
                        example: "Отсутствует JWT-токен"
        404:
            description: Объект не найден или не существует
            schema:
                type: object
                properties:
                    message:
                        type: string
                        example: "Объект не найден или не существует"
                    error:
                        type: string
                        example: "Пользователь не найден"
    """
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        raise NotFoundError("Пользователь не найден")

    return jsonify(user.to_dict()), 200


@auth.route('/refresh', methods=['POST'])
def refresh():
    """
    Обновление access-токена
    ---
    tags:
      - Authentication
    summary: Обновить access-токен
    description: Получает refresh-токен в теле запроса и возвращает новую пару токенов
    parameters:
      - name: body
        in: body
        required: true
        schema:
            type: object
            required:
              - refresh_token
            properties:
                refresh_token:
                    type: string
                    example: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
    responses:
        200:
            description: Токены обновлены
            schema:
                type: object
                properties:
                    access_token:
                        type: string
                        example: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
                    refresh_token:
                        type: string
                        example: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
        400:
            description: Нет refresh-токена
            schema:
                type: object
                properties:
                    error:
                        type: string
                        example: "Refresh-токен обязателен"
        401:
            description: Невалидный refresh-токен
            schema:
                type: object
                properties:
                    error:
                        type: string
                        example: "Невалидный refresh-токен"
    """

    data = request.get_json()
    if not data:
        raise ValidationError("Нет данных в запросе")
    
    refresh_token = data.get('refresh_token')
    if not refresh_token:
        raise ValidationError("Refresh-токен обязателен", errors={"refresh_token": "Поле обязательно"})
    
    user = User.query.filter_by(refresh_token=refresh_token).first()
    if not user:
        raise UnauthorizedError("Невалидный refresh-токен")
    
    access_token = create_access_token(identity=str(user.id), additional_claims={'role': user.role})

    new_refresh_token = create_refresh_token(identity=str(user.id))
    user.refresh_token = new_refresh_token
    db.session.commit()

    return jsonify({
        'access_token': access_token,
        'refresh_token': new_refresh_token
    }), 200


@auth.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """
    Выход из системы
    ---
    tags:
      - Authentication
    summary: Выйти из системы
    description: Удаляет refresh-токен пользователя в БД
    security:
      - Bearer: []
    responses:
        200:
            description: Успешный выход
            schema:
                type: object
                properties:
                    message:
                        type: string
                        example: "Успешно вышли из системы"
        401:
            description: Не авторизован
            schema:
                type: object
                properties:
                    error:
                        type: string
                        example: "Отсутсвует JWT-токен"
    """

    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        raise NotFoundError("Пользователь не найден")

    user.refresh_token = None
    db.session.commit()
    
    return jsonify({'message': 'Успешно вышли из системы'}), 200
