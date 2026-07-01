from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.orm import selectinload
from datetime import datetime, timezone

from app.extensions import db
from app.models.user import User
from app.models.motorcycle import Motorcycle
from app.utils.check_maintenance_status import check_status
from app.exceptions import NotFoundError

statistic = Blueprint('statistic', __name__)


@statistic.route('/dashboard-data')
@jwt_required()
def get_data():
    """
    Получить данные для дашборда
    ---
    tags:
      - Statistic
    summary: Данные дашборда
    description: Возвращает информацию о пользователе, мотоциклах и статусах планового обслуживания
    security:
      - Bearer: []
    responses:
      200:
        description: Данные успешно получены
        schema:
          type: object
          properties:
            user:
              type: object
            motorcycles:
              type: array
              items:
                type: object
                properties:
                  id: {type: integer}
                  model: {type: string}
                  mileage: {type: integer}
                  health: {type: number}
                  planned_maintenances:
                    type: array
                    items:
                      type: object
                      properties:
                        id: {type: integer}
                        title: {type: string}
                        planned_mileage: {type: integer}
                        status: {type: string, enum: ['overdue', 'soon', 'ok', 'no_mileage']}
            maintenance:
              type: array
              description: Все плановые обслуживания с их статусами
      401:
        description: Не авторизован
      404:
        description: Пользователь не найден
    """

    user = User.query.options(
      selectinload(User.motorcycles)
      .selectinload(Motorcycle.planned_maintenances)
    ).get(get_jwt_identity())

    if not user:
      raise NotFoundError("Пользователь не найден")

    motorcycle_data = []
    all_planned_maintenances = []

    for motorcycle in user.motorcycles:
      planned_records = []
      overdue_count = 0

      for plan in motorcycle.planned_maintenances:
        status = check_status(plan, motorcycle)
        planned_records.append({
          'id': plan.id,
          'title': plan.title,
          'planned_mileage': plan.planned_mileage,
          'status': status
        })

        if status == 'overdue':
          overdue_count += 1
      
      health = max(0, 100 - (overdue_count * 10))

      moto_dict = motorcycle.to_dict()
      moto_dict['health'] = round(health, 1)
      moto_dict['planned_maintenances'] = planned_records
      
      motorcycle_data.append(moto_dict)
      all_planned_maintenances.extend(planned_records)

    return jsonify({
        'user': user.to_dict(),
        'motorcycles': motorcycle_data,
        'maintenance': all_planned_maintenances
    }), 200