from flask import Blueprint, jsonify, request
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                jwt_required, get_jwt_identity)
from datetime import datetime, timedelta
import secrets

from app.exceptions import UnauthorizedError, ValidationError, ForbiddenError
from app.extensions import db
from app.models.user import User
from app.schemas.auth import LoginSchema, RefreshSchema, RegisterSchema
from app.services.user_service import UserService
from app.utils.helpers import get_current_user
from app.utils.email import send_verification_email, verify_token, verify_reset_token, send_reset_email

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

    send_verification_email(user)

    access_token = create_access_token(
        identity=str(user.id), additional_claims={"role": user.role}
    )
    refresh_token = create_refresh_token(identity=str(user.id))
    user.refresh_token = refresh_token
    db.session.commit()

    return jsonify({
        "message": "Регистрация успешна! Подтвердите email.",
        "access_token": access_token,
        "refresh_token": refresh_token,
        "user": user.to_dict(),
        "requires_verification": True
    }), 201


@auth.route("/login", methods=["POST"])
def login():
    """
    Логин пользователя
    """

    data = LoginSchema(**request.get_json())
    user = UserService.authenticate_user(email=data.email, password=data.password)

    if not(user.is_verified):
        raise ForbiddenError("Email не подтвержден. Проверьте почту")

    access_token = create_access_token(
        identity=str(user.id), additional_claims={"role": user.role}
    )
    if data.rememberMe:
        refresh_token = create_refresh_token(identity=str(user.id))
        user.refresh_token = refresh_token
        db.session.commit()

    if not(data.rememberMe) and user.refresh_token:
        user.refresh_token = None
        db.session.commit()

    return (
        jsonify(
            {
                "message": "Вы вошли в аккаунт",
                "access_token": access_token,
                "refresh_token": refresh_token if data.rememberMe else None,
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


@auth.route('/send-verification', methods=['POST'])
@jwt_required()
def send_verification():
    """Отправить письмо с подтверждением"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'Пользователь не найден'}), 404
    
    if user.is_verified:
        return jsonify({'message': 'Email уже подтвержден'}), 200
    
    send_verification_email(user)
    
    return jsonify({'message': 'Письмо отправлено'}), 200


@auth.route('/verify-email/<token>', methods=['GET'])
def verify_email(token):
    """Подтверждение email по токену"""
    email = verify_token(token)
    
    if not email:
        return jsonify({'error': 'Ссылка недействительна или истекла'}), 400
    
    user = User.query.filter_by(email=email).first()
    
    if not user:
        return jsonify({'error': 'Пользователь не найден'}), 404
    
    if user.is_verified:
        return jsonify({'message': 'Email уже подтвержден'}), 200
    
    user.is_verified = True
    db.session.commit()
    
    # Генерируем токены для автоматического входа
    access_token = create_access_token(identity=str(user.id))
    refresh_token = create_refresh_token(identity=str(user.id))
    
    return jsonify({
        'message': 'Email подтвержден!',
        'access_token': access_token,
        'refresh_token': refresh_token,
        'user': user.to_dict()
    }), 200


@auth.route('/resend-verification', methods=['POST'])
@jwt_required()
def resend_verification():
    """Отправить письмо повторно"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'Пользователь не найден'}), 404
    
    if user.is_verified:
        return jsonify({'message': 'Email уже подтвержден'}), 200
    
    send_verification_email(user)
    
    return jsonify({'message': 'Письмо отправлено повторно'}), 200


@auth.route('/check-verification', methods=['GET'])
@jwt_required()
def check_verification():
    """Проверить, подтвержден ли email"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'Пользователь не найден'}), 404
    
    return jsonify({
        'is_verified': user.is_verified
    }), 200


@auth.route('/forgot-password', methods=['POST'])
def forgot_password():
    """Запрос на сброс пароля"""
    data = request.get_json()
    email = data.get('email')
    
    if not email:
        return jsonify({'error': 'Email обязателен'}), 400
    
    user = User.query.filter_by(email=email).first()
    
    if not user:
        return jsonify({'message': 'Если такой email существует, письмо отправлено'}), 200
    
    send_reset_email(user)
    
    return jsonify({'message': 'Если такой email существует, письмо отправлено'}), 200


@auth.route('/reset-password', methods=['POST'])
def reset_password():
    """Смена пароля по токену"""
    data = request.get_json()
    token = data.get('token')
    new_password = data.get('new_password')
    
    if not token or not new_password:
        return jsonify({'error': 'Токен и новый пароль обязательны'}), 400
    
    if len(new_password) < 6:
        return jsonify({'error': 'Пароль должен быть минимум 6 символов'}), 400
    
    email = verify_reset_token(token)
    
    if not email:
        return jsonify({'error': 'Ссылка недействительна или истекла'}), 400
    
    user = User.query.filter_by(email=email).first()
    
    if not user:
        return jsonify({'error': 'Пользователь не найден'}), 404
    
    user.set_password(new_password)
    db.session.commit()
    
    return jsonify({'message': 'Пароль успешно изменён!'}), 200


@auth.route('/check-reset-token/<token>', methods=['GET'])
def check_reset_token(token):
    """Проверка валидности токена"""
    email = verify_reset_token(token)
    
    if not email:
        return jsonify({'valid': False, 'error': 'Ссылка недействительна или истекла'}), 400
    
    return jsonify({'valid': True, 'email': email}), 200