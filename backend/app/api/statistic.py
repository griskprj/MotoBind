from flask import Blueprint, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.orm import selectinload
from datetime import datetime, timedelta

from app.models.user import User
from app.models.motorcycle import Motorcycle
from app.utils.check_maintenance_status import check_status
from app.exceptions import NotFoundError, ForbiddenError, BusinessLogicError
from app.utils.maintenance_nodes import gen_maintenance_nodes
from app.utils.calculate_maintenance_money import calculate_maintenance_money, _calculate_change_percent
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
      401:
        description: Не авторизован
      404:
        description: Пользователь не найден
    """
    user_id = get_jwt_identity()
    
    user = User.query.options(
        selectinload(User.motorcycles)
        .selectinload(Motorcycle.planned_maintenances),
        selectinload(User.motorcycles)
        .selectinload(Motorcycle.maintenances)
    ).get(user_id)

    if not user:
        raise NotFoundError("Пользователь не найден")

    now = datetime.now()
    month_start = datetime(now.year, now.month, 1)
    prev_month_start = (month_start - timedelta(days=1)).replace(day=1)
    thirty_days_ago = now - timedelta(days=30)

    stats = {
        'motorcycles_count': 0,
        'plan_maintenances_count': 0,
        'maintenances_count': 0,
        'total_spends': 0,
        'new_motorcycles_count': 0,
        'month_maintenances_count': 0,
        'spends_change_percent': 0.0
    }
    
    motorcycle_data = []
    all_planned_maintenances = []
    
    current_month_spends = 0
    previous_month_spends = 0

    for motorcycle in user.motorcycles[:3]:
        if motorcycle.created_at and motorcycle.created_at >= month_start:
            stats['new_motorcycles_count'] += 1

        planned_records = []
        for plan in motorcycle.planned_maintenances[:3]:
            status = check_status(plan, motorcycle)
            plan_data = plan.to_dict()
            plan_data['status'] = status
            planned_records.append(plan_data)
            stats['plan_maintenances_count'] += 1

        recent_maintenances = sorted(
            motorcycle.maintenances, 
            key=lambda x: x.date if x.date else datetime.min, 
            reverse=True
        )[:3]

        for maintenance in recent_maintenances:
            if maintenance.cost:
                stats['total_spends'] += maintenance.cost
                stats['maintenances_count'] += 1

                if maintenance.date:
                    if maintenance.date >= month_start:
                        current_month_spends += maintenance.cost
                        stats['month_maintenances_count'] += 1
                    elif prev_month_start <= maintenance.date < month_start:
                        previous_month_spends += maintenance.cost

        moto_dict = motorcycle.to_dict()
        moto_dict['planned_maintenances'] = planned_records
        moto_dict['recent_maintenances'] = [
            m.to_dict() for m in recent_maintenances
        ]
        motorcycle_data.append(moto_dict)
        all_planned_maintenances.extend(planned_records)

    stats['spends_change_percent'] = _calculate_change_percent(
        current_month_spends, 
        previous_month_spends
    )
    
    stats['motorcycles_count'] = len(user.motorcycles)

    all_planned_maintenances.sort(
        key=lambda x: {'overdue': 0, 'soon': 1, 'ok': 2}.get(x.get('status', 'ok'), 3)
    )

    all_planned_maintenances = all_planned_maintenances[:3]

    return jsonify({
        'user': user.to_dict(),
        'motorcycles': motorcycle_data,
        'maintenance': all_planned_maintenances,
        **stats
    }), 200


def _calculate_change_percent(current: float, previous: float) -> float:
    """Вычисляет процент изменения расходов"""
    if previous > 0:
        return round(((current - previous) / previous) * 100, 1)
    elif current > 0:
        return 100.0
    return 0.0


@statistic.route('/dashboard-charts')
@jwt_required()
def get_dashboard_charts():
    """
    Получить данные для графиков на дашборде
    ---
    tags:
      - Statistic
    summary: Данные для графиков дашборда
    description: Возвращает данные для графиков затрат и частоты обслуживаний за последние 12 месяцев
    security:
      - Bearer: []
    responses:
      200:
        description: Данные успешно получены
        schema:
          type: object
          properties:
            cost_chart:
              type: array
              description: Данные для графика затрат
              items:
                type: object
                properties:
                  month: {type: string, example: "Янв 2026"}
                  value: {type: integer, example: 15000}
            count_chart:
              type: array
              description: Данные для графика частоты обслуживаний
              items:
                type: object
                properties:
                  month: {type: string, example: "Янв 2026"}
                  value: {type: integer, example: 5}
      401:
        description: Не авторизован
      404:
        description: Пользователь не найден
    """
    user = User.query.options(
        selectinload(User.motorcycles)
        .selectinload(Motorcycle.maintenances)
    ).get(get_jwt_identity())

    if not user:
        raise NotFoundError("Пользователь не найден")

    now = datetime.now()
    cost_data = []
    count_data = []
    
    month_names = ['Янв', 'Фев', 'Мар', 'Апр', 'Май', 'Июн', 
                   'Июл', 'Авг', 'Сен', 'Окт', 'Ноя', 'Дек']

    for i in range(11, -1, -1):
        month_date = now.replace(day=1) - timedelta(days=i*30)
        month_start = datetime(month_date.year, month_date.month, 1)
        
        if month_date.month == 12:
            month_end = datetime(month_date.year + 1, 1, 1)
        else:
            month_end = datetime(month_date.year, month_date.month + 1, 1)

        month_cost = 0
        month_count = 0

        for motorcycle in user.motorcycles:
            for maintenance in motorcycle.maintenances:
                if maintenance.date and month_start <= maintenance.date < month_end:
                    if maintenance.cost:
                        month_cost += maintenance.cost
                    month_count += 1

        month_label = f"{month_names[month_date.month - 1]} {month_date.year}"
        
        cost_data.append({
            'month': month_label,
            'value': month_cost
        })

        count_data.append({
            'month': month_label,
            'value': month_count
        })

    return jsonify({
        'cost_chart': cost_data,
        'count_chart': count_data
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
      401:
        description: Не авторизован
      403:
        description: Доступ запрещен
      404:
        description: Объект не найден
    """
    user_id = get_jwt_identity()
    
    moto = Motorcycle.query.options(
        selectinload(Motorcycle.planned_maintenances),
        selectinload(Motorcycle.maintenances)
    ).get(moto_id)
    
    user = User.query.get(user_id)

    if not moto:
        raise NotFoundError("Мотоцикл не найден")
    if not user:
        raise NotFoundError("Пользователь не найден")
    if int(moto.owner_id) != int(user.id):
        raise ForbiddenError("Вы не являетесь владельцем этого мотоцикла")

    try:
        planned_maintenances = sorted(
            moto.planned_maintenances,
            key=lambda x: x.planned_mileage,
            reverse=False
        )[:5]
        
        recent_maintenances = sorted(
            moto.maintenances,
            key=lambda x: x.date if x.date else datetime.min,
            reverse=True
        )[:5]
        
        nodes = gen_maintenance_nodes(moto_id, user.id)
        nodes = nodes[:5] if nodes else []
        
        cost_data = calculate_maintenance_money(moto_id, user.id)
        cost_data['chart_data'] = cost_data.get('chart_data', [])[:5]
        
        freq_data = calculate_maintenance_freq(moto_id, user.id)
        freq_data['chart_data'] = freq_data.get('chart_data', [])[:5]
        
        return jsonify({
            'motorcycle': moto.to_dict(),
            'planned_maintenances': [m.to_dict() for m in planned_maintenances],
            'recent_maintenances': [m.to_dict() for m in recent_maintenances],
            'nodes': nodes,
            
            'total_cost': cost_data.get('total_cost', 0),
            'max_cost': cost_data.get('max_cost', 0),
            'average_cost': cost_data.get('average_cost', 0),
            'month_cost': cost_data.get('month_cost', 0),
            'money_chart_data': cost_data.get('chart_data', []),
            
            'total_maintenances': freq_data.get('total_maintenances', 0),
            'month_maintenances': freq_data.get('month_maintenances', 0),
            'freq_chart_data': freq_data.get('chart_data', [])
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