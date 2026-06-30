from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime, timezone
from app.extensions import db
from app.models.user import User
from app.models.motorcycle import Motorcycle
from app.utils.check_maintenance_status import check_status


statistic = Blueprint('statistic', __name__)


@statistic.route('/dashboard-data')
@jwt_required()
def get_data():
    """
    Получить данные для отображения на дашборде пользователя, включая информацию о мотоциклах и их плановом обслуживании.
    ---
    tags:
      - Statistic
    responses:
      200:
        description: Данные успешно получены
        content:
          application/json:
            schema:
              type: object
              properties:
                user:
                  type: object
                  description: Информация о пользователе
                motorcycles:
                  type: array
                  description: Список мотоциклов пользователя с информацией о плановом обслуживании
                maintenance:
                  type: array
                  description: Список статусов планового обслуживания для каждого мотоцикла
    """
    current_user_id = int(get_jwt_identity())
    user = User.query.get(current_user_id)

    motorcycle = [m.to_dict(include_planned_maintenance=True) for m in user.motorcycles]
    planned_maintenances = []

    for moto in motorcycle:
        records = [check_status(record['id'], moto['id']) for record in moto['planned_maintenances']]

        planned_maintenances.append(records)

        overdue_maintenance = [m for m in records if m['status'] == 'overdue']
        health = 100 - (len(overdue_maintenance) * 0.1)
        moto['health'] = health

    return jsonify({
        'user': user.to_dict(),
        'motorcycles': motorcycle,
        'maintenance': planned_maintenances
    })
