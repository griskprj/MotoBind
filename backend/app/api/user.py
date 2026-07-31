from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.extensions import db
from app.models.user import User
from app.services.user_service import UserService
from app.exceptions import ValidationError, ForbiddenError

user = Blueprint('user', __name__)


@user.route('/profile', methods=['PUT'])
@jwt_required()
def udpate_profile():
    """
    Обновить профиль
    """

    current_user_id = int(get_jwt_identity())
    user = UserService.get_user_by_id(current_user_id)

    data = request.get_json()
    if not data:
        raise ValidationError("Нет данных")

    if 'username' in data:
        user.username = data.get('username')
    if 'email' in data:
        user.email = data.get('email')
    if 'bio' in data:
        user.bio = data.get('bio')

    db.session.commit()
    return jsonify(user.to_dict()), 200


@user.route('/change-password', methods=['PATCH'])
@jwt_required()
def change_password():
    """
    Изменить пароль
    """

    current_user_id = int(get_jwt_identity())
    user = UserService.get_user_by_id(current_user_id)

    data = request.get_json()
    if not data:
        raise ValidationError("Нет данных")

    if not(user.check_password(data.get('currentPassword'))):
        raise ForbiddenError("Неверный текущий пароль")

    if not(data.get('newPassword')):
        raise ValidationError("Введите новый пароль")

    user.set_password(data.get('newPassword'))
    db.session.commit()

    return jsonify(user.to_dict()), 200


@user.route('/account', methods=['DELETE'])
@jwt_required()
def delete_account():
    """
    Удалить аккаунт
    """

    current_user_id = int(get_jwt_identity())
    user = UserService.get_user_by_id(current_user_id)
    data = request.get_json()

    if not(user.check_password(data.get('password'))):
        raise ForbiddenError("Неверный пароль")

    db.session.delete(user)
    db.session.commit()

    return jsonify({'message': 'Аккаунт удален. Возвращайтесь)'}), 200
