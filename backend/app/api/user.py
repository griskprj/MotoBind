from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.exceptions import ForbiddenError, ValidationError
from app.extensions import db
from app.schemas.user import ChangePasswordSchema, UpdateProfileSchema
from app.services.user_service import UserService

user = Blueprint("user", __name__)


@user.route("/profile", methods=["PUT"])
@jwt_required()
def update_profile():
    """
    Обновить профиль
    """

    data = UpdateProfileSchema(**request.get_json())
    user = UserService.update_profile(
        user_id=int(get_jwt_identity()),
        **data.model_dump(exclude_unset=True, exclude_none=True)
    )
    return jsonify(user.to_dict()), 200


@user.route("/avatar", methods=["POST"])
@jwt_required()
def upload_avatar():
    """
    Загрузить аватар
    """
    if 'avatar' not in request.files:
        return jsonify({"error": "Файл не найден"}), 400
    
    file = request.files['avatar']
    if file.filename == '':
        return jsonify({"error": "Файл не выбран"}), 400
    
    user_id = int(get_jwt_identity())
    user = UserService.update_avatar(user_id, file)
    
    return jsonify(user.to_dict()), 200


@user.route("/avatar", methods=["DELETE"])
@jwt_required()
def delete_avatar():
    """
    Удалить аватар
    """
    user_id = int(get_jwt_identity())
    user = UserService.delete_avatar(user_id)
    
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

    # Удаляем аватар перед удалением аккаунта
    if user.avatar:
        from app.utils.files import delete_file
        delete_file(user.avatar)

    db.session.delete(user)
    db.session.commit()

    return jsonify({"message": "Аккаунт удален. Возвращайтесь)"}), 200