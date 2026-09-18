"""
Auth API — тонкие контроллеры.

Вся бизнес-логика — в app/services/auth_service.py.
"""
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from app.schemas.auth import (
    LoginSchema, RefreshSchema, RegisterSchema,
    LoginResponseSchema, RegisterResponseSchema,
    RefreshResponseSchema, VerifyEmailResponseSchema,
    UserResponseSchema, MessageResponseSchema,
    CheckVerificationResponseSchema, CheckResetTokenResponseSchema,
)
from app.services.auth_service import AuthService
from app.utils.helpers import get_current_user

auth = Blueprint("auth", __name__)


# ---- Registration / Login ----

@auth.route("/register", methods=["POST"])
def register():
    """Регистрация пользователя."""
    data = RegisterSchema.model_validate(request.get_json() or {})

    result = AuthService.register(
        email=data.email,
        password=data.password,
        username=data.username,
        role=data.role,
    )
    response = RegisterResponseSchema.model_validate(result).model_dump()
    return jsonify(response), 201


@auth.route("/login", methods=["POST"])
def login():
    """Логин пользователя."""
    data = LoginSchema.model_validate(request.get_json() or {})

    result = AuthService.login(
        email=data.email,
        password=data.password,
        remember_me=data.rememberMe,
    )
    response = LoginResponseSchema.model_validate(result).model_dump()
    return jsonify(response), 200


# ---- Current user ----

@auth.route("/me", methods=["GET"])
@jwt_required()
def get_me():
    """Данные текущего пользователя."""
    user = get_current_user()
    return jsonify(UserResponseSchema.model_validate(user).model_dump()), 200


# ---- Refresh / logout ----

@auth.route("/refresh", methods=["POST"])
def refresh():
    """Обновление access-токена."""
    data = RefreshSchema.model_validate(request.get_json() or {})

    result = AuthService.refresh(refresh_token=data.refresh_token)
    response = RefreshResponseSchema.model_validate(result).model_dump()
    return jsonify(response), 200


@auth.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    """Выход из системы."""
    user = get_current_user()
    AuthService.logout(user)
    return jsonify(MessageResponseSchema(message="Успешно вышли из системы").model_dump()), 200


# ---- Email verification ----

@auth.route("/send-verification", methods=["POST"])
@jwt_required()
def send_verification():
    """Отправить письмо с подтверждением."""
    user = get_current_user()
    message = AuthService.send_verification(user)
    return jsonify(MessageResponseSchema(message=message).model_dump()), 200


@auth.route("/verify-email/<token>", methods=["GET"])
def verify_email(token):
    """Подтверждение email по токену."""
    result = AuthService.verify_email(token=token)
    return jsonify(result), 200


@auth.route("/resend-verification", methods=["POST"])
@jwt_required()
def resend_verification():
    """Отправить письмо повторно."""
    user = get_current_user()
    message = AuthService.send_verification(user)
    return jsonify(MessageResponseSchema(message=message).model_dump()), 200


@auth.route("/check-verification", methods=["GET"])
@jwt_required()
def check_verification():
    """Проверить, подтверждён ли email."""
    user = get_current_user()
    return jsonify(CheckVerificationResponseSchema(is_verified=user.is_verified).model_dump()), 200


# ---- Password reset ----

@auth.route("/forgot-password", methods=["POST"])
def forgot_password():
    """Запрос на сброс пароля."""
    data = request.get_json() or {}
    AuthService.forgot_password(email=data.get("email"))
    return jsonify(MessageResponseSchema(message="Если такой email существует, письмо будет отправлено").model_dump()), 200


@auth.route("/reset-password", methods=["POST"])
def reset_password():
    """Смена пароля по токену."""
    data = request.get_json() or {}
    AuthService.reset_password(
        token=data.get("token"),
        new_password=data.get("new_password"),
    )
    return jsonify(MessageResponseSchema(message="Пароль успешно изменен").model_dump()), 200


@auth.route("/check-reset-token/<token>", methods=["GET"])
def check_reset_token(token):
    """Проверка валидности reset-токена."""
    email = AuthService.check_reset_token(token=token)
    return jsonify(CheckResetTokenResponseSchema(valid=True, email=email).model_dump()), 200