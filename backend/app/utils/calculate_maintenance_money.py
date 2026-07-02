from sqlalchemy.orm import selectinload
from datetime import datetime, timedelta
from collections import defaultdict

from app.extensions import db
from app.models.maintenance import Maintenance
from app.models.motorcycle import Motorcycle
from app.models.user import User
from app.exceptions import NotFoundError, ForbiddenError, BusinessLogicError

def calculate_maintenance_money(moto_id, user_id):
    """
    Возвращает данные о затратах на обслуживание: общие затраты, затраты в этом месяце, самое дорогое обслуживание, данные для графика
    """

    user = User.query.get(user_id)
    moto = Motorcycle.query.options(
        selectinload(Motorcycle.maintenances)
    ).get(moto_id)

    if not user:
        raise NotFoundError("Пользователь не найден")
    if not moto:
        raise NotFoundError("Мотоцикл не найден")

    if int(moto.owner_id) != int(user.id) and user.role != 'admin':
        raise ForbiddenError("Вы не являетесь владельцем этого мотоцикла")
    
    try:
        maintenances = moto.maintenances

        if not maintenances:
            return {
                'total_cost': 0,
                'max_cost': 0,
                'month_cost': 0,
                'average_cost': 0,
                'chart_data': []
            }

        total_cost = sum(m.cost for m in maintenances if m.cost)

        max_cost = max(m.cost for m in maintenances if m.cost)

        average_cost = total_cost / len(maintenances) if maintenances else 0

        now = datetime.now()
        month_start = datetime(now.year, now.month, 1)
        month_cost = sum(
            m.cost for m in maintenances
            if m.cost and m.date and m.date >= month_start
        )

        chart_data = []
        for i in range(11, -1, -1):
            month_date = datetime(now.year, now.month, 1) - timedelta(days=i*30)
            month_start_dt = datetime(month_date.year, month_date.month, 1)

            if month_date.month == 12:
                next_month = datetime(month_date.year + 1, 1, 1)
            else:
                next_month = datetime(month_date.year, month_date.month + 1, 1)
            
            month_total = sum(
                m.cost for m in maintenances
                if m.cost and m.date and month_start_dt <= m.date < next_month
            )
            
            chart_data.append({
                'month': month_date.strftime('%Y-%m'),
                'value': month_total
            })
        
        return {
            'total_cost': total_cost,
            'max_cost': max_cost,
            'month_cost': month_cost,
            'average_cost': round(average_cost, 2),
            'chart_data': chart_data
        }

    except Exception as e:
        raise BusinessLogicError(f'Ошибка при расчете затрат: {str(e)}')