from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime, timezone
from app.extensions import db
from app.models.user import User
from app.models.maintenance import Maintenance, PlannedMaintenance
from app.models.motorcycle import Motorcycle


maintenance = Blueprint('maintenance', __name__)


@maintenance.route('/create-new', methods=['POST'])
@jwt_required()
def create_new_maintenance():
    """ Create new maintenance record """
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Нет данных'}), 400

    user = User.query.get(get_jwt_identity())
    moto_id = data.get('motorcycleId')
    title = data.get('title')
    description = data.get('description')
    mileage = data.get('mileage')
    date = data.get('date')

    # validate required fileds
    if not title or not moto_id:
        return jsonify({'error': 'Заполните обязательные поля'}), 400

    # validate motorcycle
    motorcycle = Motorcycle.query.get(moto_id)
    if not motorcycle:
        return jsonify({'error': 'Мотоцикл не найден'}), 404

    moto_ids = [m.to_dict()['id'] for m in user.motorcycles]
    if moto_id not in moto_ids:
        return jsonify({'error': 'Вы можете добавлять обслуживание только для своего мотоцикла'}), 403
    
    # create maintenance obj
    try:
        maintenance = Maintenance(
            author_id=user.id,
            moto_id=moto_id,
            title=title,
            description=description,
            mileage=mileage,
            date=datetime.strptime(date, "%Y-%m-%d") if date else None
        )

        db.session.add(maintenance)
        db.session.commit()
        
        return jsonify(maintenance.to_dict()), 201
    except Exception as e:
        current_app.logger.error(f'Failed add maintenance: {str(e)}')
        return jsonify({'error': 'Ошибка сервера'}), 500


@maintenance.route('/plan', methods=['POST'])
@jwt_required()
def plan_maintenance():
    """ Plan maintenance record """
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Нет данных'}), 400

    user = User.query.get(get_jwt_identity())
    moto_id = data.get('motorcycleId')
    title = data.get('title')
    description = data.get('description')
    schedule_type = data.get('scheduleType')
    mileage = data.get('mileage')
    date = data.get('date')

    # validate motorcycle
    motorcycle = Motorcycle.query.get(moto_id)
    if not motorcycle:
        return jsonify({'error': 'Мотоцикл не найден'}), 404
    
    moto_ids = [m.to_dict()['id'] for m in user.motorcycles]
    if moto_id not in moto_ids:
        return jsonify({'error': 'Вы можете планировать обслуживание только для своего мотоцикла'}), 403

    # validate required fileds
    if not title or not moto_id:
        return jsonify({'error': 'Заполните обязательные поля'}), 400
    
    # validate mileage: mileage schedule type
    if schedule_type == 'mileage' and not mileage:
        return jsonify({'error': 'Пробег не указан'})
    
    if mileage and mileage < motorcycle.mileage:
        return jsonify({'error': 'Указан пробег меньше пробега мотоцикла'})

    # validate date: date schedule type
    if schedule_type == 'date' and not date:
        return jsonify({'error':'Укажите дату обслуживания'})

    date_now = datetime.now()
    if date and date_now < date:
        return jsonify({'error': 'Дата не может быть в прошлом'})

    # create maintenance obj
    try:
        maintenance = PlannedMaintenance(
            author_id=user.id,
            moto_id=moto_id,
            title=title,
            description=description,
            planned_mileage=mileage,
            planned_date=datetime.strptime(date, "%Y-%m-%d") if date else None
        )

        db.session.add(maintenance)
        db.session.commit()
        
        return jsonify(maintenance.to_dict()), 201
    except Exception as e:
        current_app.logger.error(f'Failed add maintenance: {str(e)}')
        return jsonify({'error': 'Ошибка сервера'}), 500
