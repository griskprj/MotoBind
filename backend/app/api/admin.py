from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.extensions import db
from app.exceptions import NotFoundError, ForbiddenError, ValidationError
from app.decorators import admin_required
from app.models.user import User
from app.models.motorcycle import Motorcycle
from app.models.maintenance import Maintenance
from app.models.manual import Manual
from app.models.reports import Report

admin = Blueprint('admin', __name__)

@admin.route('/get', methods=['GET'])
@jwt_required()
@admin_required
def dashboard_data():
    """
    Получение данные для админ-панели
    ---
    tags:
      - Admin
    security:
      - Bearer: []
    summary: Получение данных для админ-панели
    description: Возвращает данные о пользователях, мануалах и статистики сайта

    responses:
        201:
            description: Данные получены
    """

    users = User.query.all()
    users_count = 0
    users_data = []
    for user in users:
        users_data.append(user.to_dict(include_moto=True))
        users_count += 1

    manuals = Manual.query.filter_by(status='moderate').all()
    manuals_count = 0
    manuals_data = []
    for manual in manuals:
        manuals_count += 1
        if manual.status == 'moderate':
            manuals_data.append(manual.to_dict())
        
    motorcycles_count = len([m for m in Motorcycle.query.all()])
    
    return jsonify({
        'users': users_data,
        'manuals': manuals_data,
        'users_count': users_count,
        'manuals_count': manuals_count,
        'motorcycles_count': motorcycles_count
    }), 200

@admin.route('/manual/<int:manual_id>/approve', methods=['POST'])
@jwt_required()
@admin_required
def approve_manual(manual_id):
    """
    Одобрение мануала
    ---
    tags:
      - Admin
    security:
      - Bearer: []
    summary: Одобрение мануала
    description: Устанавливает статус мануала на 'approved'

    parameters:
      - name: manual_id
        in: path
        required: true
        type: integer
        description: ID мануала

    responses:
        200:
            description: Мануал успешно одобрен
        404:
            description: Мануал не найден
        400:
            description: Мануал уже обработан
    """
    manual = Manual.query.get(manual_id)
    if not manual:
        raise NotFoundError('Мануал не найден')
    
    if manual.status != 'moderate':
        raise ValidationError(f'Мануал уже обработан (статус: {manual.status})')
    
    manual.status = 'approved'
    db.session.commit()
    
    return jsonify({
        'message': 'Мануал успешно одобрен',
        'manual': manual.to_dict()
    }), 200

@admin.route('/manual/<int:manual_id>/reject', methods=['POST'])
@jwt_required()
@admin_required
def decline_manual(manual_id):
    """
    Одобрение мануала
    ---
    tags:
      - Admin
    security:
      - Bearer: []
    summary: Одобрение мануала
    description: Устанавливает статус мануала на 'declined'

    parameters:
      - name: manual_id
        in: path
        required: true
        type: integer
        description: ID мануала

    responses:
        200:
            description: Мануал успешно одобрен
        404:
            description: Мануал не найден
        400:
            description: Мануал уже обработан
    """

    manual = Manual.query.get(manual_id)
    if not manual:
        raise NotFoundError("Мануал не найден")
    
    if manual.status != 'moderate': 
        raise ValidationError(f"Мануал уже обработан (статус: {manual.status})")
    
    data = request.get_json()
    if not data:
        raise ValidationError("Нет данных")
    
    reason = data.get('reazon', 'Без указания причины')

    manual.status = 'rejected'
    manual.rejection_reason = reason

    db.session.commit()

    return jsonify({
        'message': 'Мануал отклонен',
        'manual': manual.to_dict()
    }), 200

@admin.route('/manual/<int:manual_id>/reconsider', methods=['POST'])
@jwt_required()
@admin_required
def reconsider_manual(manual_id):
    """
    Пересмотр мануала
    ---
    tags:
      - Admin
    security:
      - Bearer: []
    summary: Пересмотр мануала
    description: Возвращает мануал на проверку (статус 'moderate')

    parameters:
      - name: manual_id
        in: path
        required: true
        type: integer
        description: ID мануала

    responses:
        200:
            description: Мануал возвращен на проверку
        404:
            description: Мануал не найден
        400:
            description: Мануал уже на проверке
    """

    manual = Manual.query.get(manual_id)
    if not manual:
        raise NotFoundError("Мануал не найден")
    

    if manual.status == 'moderate':
        raise ValidationError("Мануал уже на проверке")
    
    manual.status = 'moderate'
    manual.rejection_reason = None
    db.session.commit()

    return jsonify({
        'message': 'Мануал возвращен на проверку',
        'manual': manual.to_dict()
    }), 200

@admin.route('/manual/<int:manual_id>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_manual(manual_id):
    """
    Удаление мануала
    ---
    tags:
      - Admin
    security:
      - Bearer: []
    summary: Удаление мануала
    description: Полностью удаляет мануал из базы данных

    parameters:
      - name: manual_id
        in: path
        required: true
        type: integer
        description: ID мануала

    responses:
        200:
            description: Мануал успешно удален
        404:
            description: Мануал не найден
    """

    manual = Manual.query.get(manual_id)
    if not manual:
        raise NotFoundError("Мануал не найден")
    
    db.session.delete(manual)
    db.session.commit()

    return jsonify({
        'message': 'Мануал удален',
    }), 200

@admin.route('/user/<int:user_id>/ban', methods=['POST'])
@jwt_required()
@admin_required
def ban_user(user_id):
    """
    Блокировка пользователя
    ---
    tags:
      - Admin
    security:
      - Bearer: []
    summary: Блокировка пользователя
    description: Блокирует пользователя

    parameters:
      - name: user_id
        in: path
        required: true
        type: integer
        description: ID пользователя

    responses:
        200:
            description: Пользователь заблокирован
        404:
            description: Пользователь не найден
        400:
            description: Нельзя заблокировать админа или себя
    """

    user = User.query.get(user_id)
    if not user:
        raise NotFoundError("Пользователь не найден")

    current_user_id = int(get_jwt_identity())
    if int(user.id) == current_user_id:
        raise ValidationError("Нельзя заблокировать самого себя")
    
    user.status = 'banned'
    db.session.commit()

    return jsonify({
        'message': f'Пользователь {user.username} заблокирован',
        'user': user.to_dict()
    }), 200

@admin.route('/user/<int:user_id>/unban', methods=['POST'])
@jwt_required()
@admin_required
def unban_user(user_id):
    """
    Разблокировка пользователя
    ---
    tags:
      - Admin
    security:
      - Bearer: []
    summary: Разблокировка пользователя
    description: Разблокирует пользователя

    parameters:
      - name: user_id
        in: path
        required: true
        type: integer
        description: ID пользователя

    responses:
        200:
            description: Пользователь разблокирован
        404:
            description: Пользователь не найден
    """

    user = User.query.get(user_id)
    if not user:
        raise NotFoundError("Пользователь не найден")
    
    user.status = 'active'
    db.session.commit()

    return jsonify({
        'message': f'Пользователь {user.username} разблокирован',
        'user': user.to_dict()
    }), 200

@admin.route('/user/<int:user_id>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_user(user_id):
    """
    Удаление пользователя
    ---
    tags:
      - Admin
    security:
      - Bearer: []
    summary: Удаление пользователя
    description: Полностью удаляет пользователя из базы данных

    parameters:
      - name: user_id
        in: path
        required: true
        type: integer
        description: ID пользователя

    responses:
        200:
            description: Пользователь успешно удален
        404:
            description: Пользователь не найден
        400:
            description: Нельзя удалить админа или себя
    """
     
    user = User.query.get(user_id)
    if not user:
        raise NotFoundError("Пользователь не найден")
    
    current_user_id = int(get_jwt_identity())
    if int(user.id) == current_user_id:
        raise ValidationError("Нельзя удалить самого себя")
    
    db.session.delete(user)
    db.session.commit()

    return jsonify({
        'message': f'Пользователь {user.username} удален'
    }), 200