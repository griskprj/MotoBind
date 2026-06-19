from flask import Blueprint, jsonify, request, current_app, send_from_directory
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime, timezone
from app.extensions import db
from app.models.user import User
from app.models.motorcycle import Motorcycle
from app.utils.files import allowed_file, save_moto_photo


motorcycle = Blueprint('motorcycle', __name__)


@motorcycle.route('/my', methods=['GET'])
@jwt_required()
def get_user_moto():
    """ Get user motorcycles """
    current_user_id = int(get_jwt_identity())

    try:
        user = User.query.get(current_user_id)
        if not user:
            return jsonify({'error': 'Пользователь не найден'}), 404
        
        motorcycles = [m.to_dict() for m in user.motorcycles]
    except Exception as e:
        current_app.logger.error(f'Get motorcycle failed: {str(e)}')
        return jsonify({'error': 'Ошибка сервера'}), 500

    return jsonify(motorcycles), 200


@motorcycle.route('/new', methods=['POST'])
@jwt_required()
def create_moto():
    """ Create new moto """
    data = request.get_json()

    name = data.get('name')
    years = data.get('years')
    volume = data.get('volume')
    mileage = data.get('mileage')
    color = data.get('color')
    license_plate = data.get('license_plate')
    vin = data.get('vin')

    if not name:
        return jsonify({'error': 'Название мотоцикла обязательно'}), 400
    
    if color and color[0] != '#' and len(color.split('#')[1]) < 3:
        return jsonify({'error': 'Цвет должен быть формата HEX (#FFFFFF)'}), 400

    if license_plate and license_plate and len(license_plate) > 9:
        return jsonify({'error': 'Неверный формат ГОС номера'}), 400

    if vin and len(vin) != 17:
        return jsonify({'error': 'Неверный формат VIN'})

    if mileage > 1_000_000:
        return jsonify({'error': 'Введите корректный пробег'}), 400

    motorcycle = Motorcycle(
        owner_id=get_jwt_identity(),
        name=name,
        years=years,
        volume=volume,
        mileage=mileage,
        color=color,
        license_plate=license_plate,
        vin=vin
    )
    db.session.add(motorcycle)
    db.session.commit()

    return jsonify(motorcycle.to_dict()), 201


@motorcycle.route('/<int:moto_id>', methods=['PUT'])
@jwt_required()
def update_moto(moto_id):
    """ Update motorcycle """
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Нет данных'}), 400
    
    motorcycle = Motorcycle.query.get(moto_id)
    if not motorcycle:
        return jsonify({'error': 'Мотоцикл не найден'}), 404

    now = datetime
    try:
        name = data.get('name')
        volume = data.get('volume')
        mileage = data.get('mileage')
        years = data.get('years')
        if 'name' in data:
            motorcycle.name = name
        if 'years' in data and datetime.now().year > years:
            motorcycle.years = years
        if 'volume' in data and 49 <= volume <= 4000:
            motorcycle.volume = volume
        if 'mileage' in data and mileage < 1_000_000:
            motorcycle.mileage = mileage
        
        db.session.commit()
    except Exception as e:
        current_app.logger.error(f'Failed update moto: {str(e)}')
        return jsonify({'error': 'Ошибка сервера'}), 500

    return jsonify(motorcycle.to_dict())


@motorcycle.route('/<int:moto_id>', methods=['PATCH'])
@jwt_required()
def update_moto_mileage(moto_id):
    """ Update moto mileage """
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Нет данных'}), 400
    
    motorcycle = Motorcycle.query.get(moto_id)
    if not motorcycle:
        return jsonify({'error': 'Мотоцикл не найден'}), 404
    
    new_mileage = data.get('newMileage')
    if not new_mileage:
        return jsonify({'error': 'Укажите новый пробег'}), 400
    
    motorcycle.mileage = new_mileage
    db.session.commit()

    return jsonify({'message': 'Пробег обновлен'}), 200


@motorcycle.route('/<int:moto_id>', methods=['DELETE'])
@jwt_required()
def delete_moto(moto_id):
    """ Delete motorcycle """
    motorcycle = Motorcycle.query.get(moto_id)
    if not motorcycle:
        return jsonify({'error': 'Мотоцикл не найден'}), 404
    
    try:
        db.session.delete(motorcycle)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(f'Failed delete moto {str(e)}')
        return jsonify({'error': 'Ошибка сервера'}), 500

    return jsonify({'message': 'Мотоцикл удален'}), 200
