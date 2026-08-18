from flask import Blueprint, jsonify, request
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                jwt_required)

from app.exceptions import UnauthorizedError, ValidationError
from app.extensions import db
from app.models.user import User
from app.schemas.auth import LoginSchema, RefreshSchema, RegisterSchema
from app.services.user_service import UserService
from app.utils.helpers import get_current_user

auth = Blueprint("auth", __name__)


@auth.route("/register", methods=["POST"])
def register():
    """
    Регистрация пользователя
    """

    data = RegisterSchema(**request.get_json())

    try:
        user = UserService.create_user(
            email=data.email, 
            password=data.password, 
            username=data.username, 
            role=data.role
        )

        return jsonify({
            "message": "Регистрация успешна",
            "user_id": user.id,
            "email": user.email,
            "is_verified": user.is_verified,
            "verification_send": True
        }), 201
    
    except ValidationError as e:
        return jsonify({"error": str(e)}), 400


@auth.route("/veify", methods=["POST"])
def verify_email():
    """
    Подтверждение email по коду
    """
    data = request.get_json()

    email = data.get("email")
    code = data.get("code")

    if not email or not code:
        return jsonify({"error": "Email и код обязательны"}), 400

    try:
        user = UserService.verify_email(email, code)

        access_token = create_access_token(
            identity=str(user.id),
            additional_claims={"role": user.rol}
        )
        refresh_token = create_refresh_token(identity=str(user.id))
        user.refresh_token = refresh_token
        db.session.commit()

        return jsonify({
            "message": "Email успешно подтвержден",
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": user.to_dict()
        }), 200
    except ValidationError as e:
        return jsonify({"error": str(e)}), 400

@auth.route("/resend-verification", methods=["POST"])
def resend_verification():
    """
    Отправить код повторно
    """
    data = request.get_json()
    email = data.get("email")

    if not email:
        return jsonify({"error": "Email обязателен"}), 400


    try:
        result = UserService.resend_verification_code(email)
        return jsonify(result), 200
    except ValidationError as e:
        return jsonify({"error": str(e)}), 400


@auth.route("/login", methods=["POST"])
def login():
    """
    Логин пользователя
    """

    data = LoginSchema(**request.get_json())
    user = UserService.authenticate_user(email=data.email, password=data.password)

    if not user.is_verified:
        return jsonify({
            "error": "Email не подтвержден. Проверьте почту или запросите новый код.",
            "needs_verification": True,
            "email": user.email
        }), 403

    access_token = create_access_token(
        identity=str(user.id), additional_claims={"role": user.role}
    )
    if data.rememberMe:
        refresh_token = create_refresh_token(identity=str(user.id))
        user.refresh_token = refresh_token
        db.session.commit()
    else:
        if user.refresh_token:
            user.refresh_token = None
            db.session.commit()

    return (
        jsonify(
            {
                "message": "Вы вошли в аккаунт",
                "access_token": access_token,
                "refresh_token": refresh_token,
                "user": user.to_dict(),
            }
        ),
        200,
    )

@auth.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    """
    Выход из системы
    """

    user = get_current_user()
    UserService.clear_refresh_token(user)

    return jsonify({"message": "Успешно вышли из системы"}), 200



@auth.route("/me", methods=["GET"])
@jwt_required()
def get_me():
    """
    Получение данных текущего пользователя
    """
    user = get_current_user()
    return jsonify(user.to_dict()), 200


@auth.route("/refresh", methods=["POST"])
def refresh():
    """
    Обновление access-токена
    """

    data = RefreshSchema(**request.get_json())

    refresh_token = data.refresh_token
    if not refresh_token:
        raise ValidationError(
            "Refresh-токен обязателен", errors={"refresh_token": "Поле обязательно"}
        )

    user = User.query.filter_by(refresh_token=refresh_token).first()
    if not user:
        raise UnauthorizedError("Невалидный refresh-токен")

    access_token = create_access_token(
        identity=str(user.id), additional_claims={"role": user.role}
    )

    new_refresh_token = create_refresh_token(identity=str(user.id))
    user.refresh_token = new_refresh_token
    db.session.commit()

    return (
        jsonify({"access_token": access_token, "refresh_token": new_refresh_token}),
        200,
    )


@auth.route("/request-password-reset", methods=["POST"])
def request_password_reset():
    """
    Запрос на сброс пароля
    """
    data = request.get_json()
    email = data.get("email")

    if not email:
        return jsonify({"error": "Email обязателен"}), 400

    try:
        result = UserService.request_password_reset(email)
        return jsonify(result), 200
    except ValidationError as e:
        return jsonify({"error": str(e)}), 400

@auth.route("/reset-password", methods=["POST"])
def reset_password():
    """
    Сброс пароля по коду
    """
    data = request.get_json()

    email = data.get("email")
    code = data.get("code")
    new_password = data.get("new_password")

    if not email or not code or not new_password:
        return jsonify({"error": "Все поля обязательны"}), 400

    if len(new_password) < 6:
        return jsonify({"error": "Пароль должен быть не менее 6 символов"}), 400

    try:
        user = UserService.reset_password(email, code, new_password)
        return jsonify({
            "message": "Пароль успешно изменен",
            "user_id": user.id
        }), 200
    except ValidationError as e:
        return jsonify({"error": str(e)}), 400