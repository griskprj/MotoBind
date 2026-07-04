from sqlalchemy.orm import selectinload
from datetime import datetime, timedelta
from collections import defaultdict

from app.extensions import db
from app.models.maintenance import Maintenance
from app.models.motorcycle import Motorcycle
from app.models.user import User
from app.exceptions import NotFoundError, ForbiddenError, BusinessLogicError


def calculate_maintenance_freq(moto_id, user_id):
    """
    Возвращает данные о частоте обслуживаний: всего обслуживаний, обслуживаний в этом месяце, данные для графика
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
                'total_maintenances': 0,
                'month_maintenances': 0,
                'chart_data': []
            }
        
        total_maintenances = len(maintenances)

        now = datetime.now()
        month_start = datetime(now.year, now.month, 1)
        month_maintenances = len(
            [m for m in maintenances
            if m.date and m.date >= month_start]
        )

        chart_data = []
        for i in range(11, -1, -1):
            month_date = datetime(now.year, now.month, 1) - timedelta(days=i*30)
            month_start_dt = datetime(month_date.year, month_date.month, 1)

            if month_date.month == 12:
                next_month = datetime(month_date.year + 1, 1, 1)
            else:
                next_month = datetime(month_date.year, month_date.month + 1, 1)

            month_total = len(
                [m for m in maintenances
                if m.date and month_start_dt <= m.date < next_month]
            )

            chart_data.append({
                'month': month_date.strftime('%Y-%m'),
                'value': month_total
            })

        return {
            'total_maintenances': total_maintenances,
            'month_maintenances': month_maintenances,
            'chart_data': chart_data
        }
    except Exception as e:
        raise BusinessLogicError(f"Ошибка при расчете частоты обслуживани: {str(e)}")