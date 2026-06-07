from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import (
    create_access_token, create_refresh_token,
    jwt_required, get_jwt_identity
)
from app.models.user import User
from app.extensions import db


auth = Blueprint('auth', __name__)


@auth.route('/register', methods=['POST'])
def register():
    """ Зарегистрировать новую учетную запись """
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Нет данных'}), 400

    email = data.get('email')
    password = data.get('password')
    username = data.get('username')
    role = data.get('role')

    if not all([email, password, username, role]):
        return jsonify({'error': 'Заполните обязательные поля'}), 400
    
    if len(password) < 6:
        return jsonify({'error': 'Длина пароля не менее 6 символов'}), 400

    if User.query.filter_by(email=email).first():
        print("EMAIL")
        return jsonify({'error': 'Аккаунт с такой почтой уже зарегистрирован'}), 409
    if User.query.filter_by(username=username).first():
        print("USERNAME")
        return jsonify({'error': 'Имя пользователя занято'}), 409

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
        return jsonify({'error': 'Ошибка сервера'}), 500


@auth.route('/login', methods=['POST'])
def login():
    """ Login user """
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Нет данных'}), 400
    
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Почта и пароль обязательны'}), 400

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'error': 'Пользователь с такой почтой не найден'}), 404
    if not user.check_password(password):
        return jsonify({'error': 'Неправильный пароль'}), 401
    
    access_token = create_access_token(identity=str(user.id), additional_claims={'role': user.role})
    refresh_token = create_refresh_token(identity=str(user.id))

    user.refresh_token = refresh_token
    db.session.commit()

    return jsonify({
        'acces_token': access_token,
        'refresh_token': refresh_token,
        'user': user.to_dict()
    }), 200


@auth.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """ Get current user """
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'Пользователь не найден'}), 404

    return jsonify(user.to_dict()), 200


@auth.route('/refresh', methods=['POST'])
def refresh():
    """ Update access-token """
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Нет данных'}), 400
    
    refresh_token = data.get('refresh_token')
    if not refresh_token:
        return jsonify({'error': 'Refresh-токен обязателен'}), 400
    
    user = User.query.filter_by(refresh_token=refresh_token).first()
    if not user:
        return jsonify({'error': 'Невалидный refresh-токен'})
    
    access_token = create_access_token(identity=str(user.id), additional_claims={'role': user.role})

    new_refresh_token = create_refresh_token(identity=str(user.id))
    user.refresh_token = new_refresh_token
    db.session.commit()

    return jsonify({
        'access_token': access_token,
        'refresh_token': refresh_token
    }), 200


@auth.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """ Logout - delete user refresh-token """
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if user:
        user.refresh_token = None
        db.session.commit()
    
    return jsonify({'message': 'Успешно вышли из системы'}), 200
