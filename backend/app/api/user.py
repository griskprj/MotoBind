from app.exceptions import ForbiddenError
from app.extensions import db
from app.schemas.user import ChangePasswordSchema, UpdateProfileSchema
from app.services.user_service import UserService
from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

user = Blueprint("user", __name__)


@user.route("/profile", methods=["PUT"])
@jwt_required()
def udpate_profile():
    """
    Обновить профиль
    """

    data = UpdateProfileSchema(**request.get_json())
    user = UserService.update_profile(
        user_id=int(get_jwt_identity()),
        **data.model_dump(exclude_unset=True, exclude_none=True)
    )
    return jsonify(user.to_dict()), 200


@user.route("/change-password", methods=["PATCH"])
@jwt_required()
def change_password():
    """
    Изменить пароль
    """

    data = ChangePasswordSchema(**request.get_json())
    user = UserService.change_password(
        user_id=int(get_jwt_identity()),
        current_password=data.currentPassword,
        new_password=data.newPassword,
    )
    return jsonify(user.to_dict()), 200


@user.route("/account", methods=["DELETE"])
@jwt_required()
def delete_account():
    """
    Удалить аккаунт
    """

    current_user_id = int(get_jwt_identity())
    user = UserService.get_user_by_id(current_user_id)
    data = request.get_json()

    if not (user.check_password(data.get("password"))):
        raise ForbiddenError("Неверный пароль")

    db.session.delete(user)
    db.session.commit()

    return jsonify({"message": "Аккаунт удален. Возвращайтесь)"}), 200
