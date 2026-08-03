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
    user = UserService.create_user(
        email=data.email, password=data.password, username=data.username, role=data.role
    )

    return jsonify({"message": "Регистрация успешна", "user": user.to_dict()}), 201


@auth.route("/login", methods=["POST"])
def login():
    """
    Логин пользователя
    """

    data = LoginSchema(**request.get_json())
    user = UserService.authenticate_user(email=data.email, password=data.password)

    access_token = create_access_token(
        identity=str(user.id), additional_claims={"role": user.role}
    )
    refresh_token = create_refresh_token(identity=str(user.id))

    user.refresh_token = refresh_token
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


@auth.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    """
    Выход из системы
    """

    user = get_current_user()
    UserService.clear_refresh_token(user)

    return jsonify({"message": "Успешно вышли из системы"}), 200
