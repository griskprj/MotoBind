from flask import Blueprint, jsonify, request, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
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


@motorcycle.route('/', methods=['POST'])
@jwt_required()
def create_moto():
    """ Create new moto """
    name = request.form.get('name')
    years = request.form.get('years')
    volume = request.form.get('volume')
    color = request.form.get('color')
    license_plate = request.form.get('license_plate')
    vin = request.form.get('vin')

    if not name:
        return jsonify({'error': 'Название мотоцикла обязательно'}), 400
    
    if color and color[0] != '#' and len(color.split('#')[1]) < 3:
        return jsonify({'error': 'Цвет должен быть формата HEX (#FFFFFF)'}), 400

    if license_plate and license_plate and len(license_plate) > 9:
        return jsonify({'error': 'Неверный формат ГОС номера'}), 400

    if vin and len(vin) != 17:
        return jsonify({'error': 'Неверный формат VIN'})

    motorcycle = Motorcycle(
        owner_id=get_jwt_identity(),
        name=name,
        years=years,
        volume=volume,
        color=color,
        license_plate=license_plate,
        vin=vin
    )
    db.session.add(motorcycle)
    db.session.commit()

    file = request.files.get('file')
    if file and allowed_file(file.filename):
        relative_path = save_moto_photo(file, motorcycle.id)
        if relative_path:
            motorcycle.photo_url = relative_path
            db.session.commit()
        
    return jsonify(motorcycle.to_dict()), 201
