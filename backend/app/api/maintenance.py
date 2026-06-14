from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime, timezone
from app.extensions import db
from app.models.user import User
from app.models.maintenance import Maintenance
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

    if not title or not moto_id:
        return jsonify({'error': 'Заполните обязательные поля'}), 400

    moto_ids = [m.to_dict()['id'] for m in user.motorcycles]

    if moto_id not in moto_ids:
        return jsonify({'error': 'Вы можете добавлять обслуживание только для своего мотоцикла'}), 403
    
    try:
        maintenance = Maintenance(
            author_id=user.id,
            moto_id=moto_id,
            title=title,
            description=description,
            mileage=mileage,
            date=datetime.strptime(date, "%Y-%m-%d")
        )

        db.session.add(maintenance)
        db.session.commit()
        
        return jsonify(maintenance.to_dict()), 201
    except Exception as e:
        current_app.logger.error(f'Failed add maintenance: {str(e)}')
        return jsonify({'error': 'Ошибка сервера'}), 500
