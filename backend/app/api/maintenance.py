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

    # create maintenance obj
    try:
        maintenance = PlannedMaintenance(
            author_id=user.id,
            moto_id=moto_id,
            title=title,
            description=description,
            planned_mileage=mileage,
        )

        db.session.add(maintenance)
        db.session.commit()
        
        return jsonify(maintenance.to_dict()), 201
    except Exception as e:
        current_app.logger.error(f'Failed add maintenance: {str(e)}')
        return jsonify({'error': 'Ошибка сервера'}), 500


@maintenance.route('/plan', methods=['PUT'])
@jwt_required()
def edit_plan_maintenance():
    """ Edit plan maintenance """
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Нет данных'}), 400

    maintenance_id = data.get('maintenanceId')
    motorcycle_id = data.get('motorcycleId')
    title = data.get('title')
    description = data.get('description')
    mileage = data.get('mileage')

    if not maintenance_id:
        return jsonify({'error': 'Нет id обслуживания'}), 400

    maintenance = PlannedMaintenance.query.get(maintenance_id)
    if not maintenance:
        return jsoinfy({'error': 'Обслуживание не найдено'}), 404
    
    if motorcycle_id:
        maintenance.moto_id = motorcycle_id
    if title:
        maintenance.title = title
    if description:
        maintenance.description = description
    if mileage:
        maintenance.planned_mileage = mileage

    db.session.commit()

    return jsonify(maintenance.to_dict())


@maintenance.route('/plan/<int:maintenance_id>', methods=['DELETE'])
@jwt_required()
def delete_plan_maintenance(maintenance_id):
    """ Delete plan maintenance record """
    maintenance = PlannedMaintenance.query.get(maintenance_id)
    current_user_id = int(get_jwt_identity())

    if maintenance.author_id != current_user_id:
        return jsonify({'error': 'Вы можете удалять только свои записи'}), 403
    
    db.session.delete(maintenance)
    db.session.commit()

    return jsonify({'message': 'Запись удалена'}), 200


@maintenance.route('/plan/mark', methods=['POST'])
@jwt_required()
def mark_maintenance():
    """ Mark maintenance and create new if is repeat """
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Нет данных'}), 400
    
    maintenance_id = data.get('maintenanceId')
    mileage = data.get('mileage')
    date = data.get('date')
    is_repeat = data.get('isRepeat')
    interval = data.get('interval')
    current_user_id = int(get_jwt_identity())

    if not maintenance_id or not mileage:
        return jsonify({'error': 'Заполните обязательные поля'}), 400
    
    now = datetime.now()
    date_obj = datetime.strptime(date, '%Y-%m-%d')
    if date_obj > now:
        return jsonify({'error': 'Дата не может быть в будущем'}), 400
    
    if is_repeat and not interval:
        return jsonify({'error': 'Укажите интервал обслуживания'}), 400
    
    maintenance = PlannedMaintenance.query.get(maintenance_id)
    if not maintenance:
        return jsonify({'error': 'Обслуживание не найдено'}), 404
    
    moto = Motorcycle.query.get(maintenance.moto_id)

    new_maintenance = Maintenance(
        moto_id=moto.id,
        author_id=current_user_id,
        title=maintenance.title,
        description=maintenance.description,
        mileage=mileage,
        date=date_obj
    )
    if mileage > moto.mileage:
        moto.mileage = mileage

    db.session.add(new_maintenance)

    if is_repeat:
        planned_mileage = moto.mileage + interval
        planned_maintenance = PlannedMaintenance(
            author_id=current_user_id,
            moto_id=moto.id,
            title=maintenance.title,
            description=maintenance.description,
            planned_mileage=planned_mileage,
        )
        db.session.add(planned_maintenance)
    
    db.session.delete(maintenance)
    db.session.commit()

    return jsonify({
        'maintenance_record': new_maintenance.to_dict(),
        'planned_maintenance': planned_maintenance.to_dict()
    }), 201
