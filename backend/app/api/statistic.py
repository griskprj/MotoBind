from flask import Blueprint, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.orm import selectinload

from app.models.user import User
from app.models.motorcycle import Motorcycle
from app.utils.check_maintenance_status import check_status
from app.exceptions import NotFoundError, ForbiddenError, BusinessLogicError
from app.utils.maintenance_nodes import gen_maintenance_nodes
from app.utils.calculate_maintenance_money import calculate_maintenance_money
from app.utils.calculate_freq_maintenance import calculate_maintenance_freq

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
          'moto_name': motorcycle.name,
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


@statistic.route('/garage', methods=['GET'])
@jwt_required()
def get_garage_stat():
  """
  Получить данные для гаража
  ---
  tags:
    - Statistic
  summary: Данные гаража
  description: Возвращает информацию о кол-ве выполненных и запланированных обслуживаниях, id и название мотоциклов пользователя и общую сумму затрат на обслуживание.
  security:
    - Bearer: []
  responses:
    200:
      description: Данные успешно получены
      schema:
        type: object
        properties:
          motorcycles:
            type: array
            items:
              type: object
              properties:
                id: {type: integer}
                name: {type: string}
          plan_maintenances_count:
            type: integer
            description: Кол-во плановых обслуживаний
          maintenances_count:
            type: integer
            description: Кол-во выполненных обслуживаний
    401:
      description: Не авторизован
    404:
      description: Объект не найден
  """

  try:
    user = User.query.options(
      selectinload(User.motorcycles).selectinload(Motorcycle.planned_maintenances),
      selectinload(User.motorcycles).selectinload(Motorcycle.maintenances)
    ).get(get_jwt_identity())
    
    if not user:
      raise NotFoundError("Пользователь не найден")

    motorcycle = Motorcycle.query.filter_by(owner_id=user.id).all()
    if not motorcycle:
      raise NotFoundError("Мотоцикл не найден")

    planned_maintenances = []
    maintenances = []
    moto_data = []
    cost = 0
    for m in motorcycle:
      moto_data.append({'id': m.id, 'name': m.name})
      planned_maintenances.extend(m.planned_maintenances)
      maintenances.extend(m.maintenances)

      for maintenance in m.maintenances:
          cost += maintenance.cost

    return jsonify({
      'motorcycles': moto_data,
      'cost': cost,
      'plan_maintenances_count': len(planned_maintenances),
      'maintenances_count': len(maintenances)
    }), 200
  except Exception as e:
    current_app.logger.error(f'Failed load garage data: {str(e)}')
    raise BusinessLogicError("Ошибка загрузки данных для гаража")

  
@statistic.route('/garage/<int:moto_id>', methods=['GET'])
@jwt_required()
def get_moto_garage(moto_id):
  """
  Получить данные о мотоцикле для гаража
  ---
  tags:
    - Statistic
  summary: Данные мотоцикла для гаража
  description: Возвращает информацию о мотоцикле, узлах обслуживания и всех типах обслуживания
  security:
    - Bearer: []
  parameters:
    - in: path
      name: moto_id
      required: true
      type: integer
      description: Идентификатор мотоцикла
  responses:
    200:
      description: Данные успешно получены
      schema:
        type: object
        properties:
          motorcycle:
            type: object
            properties:
              id: {type: integer}
              model: {type: string}
              mileage: {type: integer}
              health: {type: number}
          maintenance_nodes:
            type: array
            items:
              node:
                type: object
                properties:
                  title: {type: string}
                  health: {type: integer}
                  maintenance_count: {type: integer}
                  planned_maintenances:
                    type: array
                    items:
                      type: object
                      properties:
                        id: {type: integer}
                        title: {type: string}
                        planned_mileage: {type: integer}
                        status: {type: string, enum: ['overdue', 'soon', 'ok', 'no_mileage']}
          moneyData:
            type: object
            properties:
              month: {type: string}
              value: {type: integer}
          maintenance_count_data:
            type: object
            properties:
              month: {type: string}
              value: {type: integer}
  """

  moto = Motorcycle.query.options(
      selectinload(Motorcycle.planned_maintenances)
  ).get(moto_id)
  user = User.query.get(get_jwt_identity())

  if not moto:
      raise NotFoundError("Мотоцикл не найден")  

  if not user:
      raise NotFoundError("Пользователь не найден")

  if int(moto.owner_id) != int(user.id):
      raise ForbiddenError("Вы не являетесь владельцем этого мотоцикла")

  try:
      nodes = gen_maintenance_nodes(moto_id, user.id)
      cost_data = calculate_maintenance_money(moto_id, user.id)
      freq_data = calculate_maintenance_freq(moto_id, user.id)
      
      return jsonify({
          'nodes': nodes,
          'motorcycle': moto.to_dict(),
          'planned_maintenances': [m.to_dict() for m in moto.planned_maintenances],
          'total_cost': cost_data['total_cost'],
          'max_cost': cost_data['max_cost'],
          'average_cost': cost_data['average_cost'],
          'month_cost': cost_data['month_cost'],
          'money_chart_data': cost_data['chart_data'],

          'total_maintenances': freq_data['total_maintenances'],
          'month_maintenances': freq_data['month_maintenances'],
          'freq_chart_data': freq_data['chart_data']
      }), 200
  except Exception as e:
      current_app.logger.error(f'Failed load garage moto data: {str(e)}')
      raise BusinessLogicError("Ошибка загрузки данных мотоцикла")

@statistic.route('/repair', methods=['GET'])
@jwt_required()
def get_stat_repair():
  """
  Получение статистики для страницы ремонта
  ---
  tags:
    - Statistic
  summary: Получение статистики для страницы ремонта
  description: Возврщает информацию о кол-ве просроченных, скорых и запланированных обсл.
  security:
    - Bearer: []
  responses:
    200:
      description: Данные успешно получены
      schema:
        type: object
        properties:
          overdue:
            type: integer
          soon:
            type: integer
          planned:
            type: integer
    404:
      description: Пользователь не найден
  """

  user = User.query.options(
    selectinload(User.motorcycles)
    .selectinload(Motorcycle.planned_maintenances)
  ).get(get_jwt_identity())

  if not user:
    raise NotFoundError("Пользователь не найден")
  
  overdue = 0
  soon = 0
  planned = 0
  motorcycles = []
  maintenances = []
  try:
    for moto in user.motorcycles:
      for plan in moto.planned_maintenances:
        status = check_status(plan, moto)
        
        match status:
          case 'ok':
            planned += 1
          case 'overdue':
            overdue += 1
          case 'soon':
            soon += 1
        
        maintenances.append(plan.to_dict())
      
      motorcycles.append(moto.to_dict())
  except Exception as e:
    current_app.logger.error(f'Failed load repair data: {str(e)}')
    raise BusinessLogicError("Ошибка сервера")
    
  return jsonify({
    'overdue': overdue,
    'soon': soon,
    'planned': planned,
    'motorcycles': motorcycles,
    'maintenances': maintenances
  }), 200