from app.exceptions import BusinessLogicError
from app.utils.statistics_helpers import (
    aggregate_by_month,
    first_day_of_month,
    get_owned_motorcycle_or_403,
    is_in_month,
)


def calculate_maintenance_freq(moto_id: int, user_id: int) -> dict:
    """
    Возвращает статистику по частоте обслуживаний:
    - всего обслуживаний
    - обслуживаний в текущем месяце
    - данные для графика за 12 месяцев (по completed_date)
    """
    try:
        moto = get_owned_motorcycle_or_403(moto_id, user_id)
        maintenances = moto.maintenances

        completed = [m for m in maintenances if m.completed_date is not None]

        if not completed:
            return {
                "total_maintenances": 0,
                "month_maintenances": 0,
                "chart_data": [],
            }

        total_maintenances = len(completed)
        month_start = first_day_of_month()

        month_maintenances = sum(1 for m in completed if is_in_month(m.completed_date, month_start))

        chart_data = aggregate_by_month(
            completed,
            date_getter=lambda m: m.completed_date,
            value_getter=lambda m: 1,
        )

        return {
            "total_maintenances": total_maintenances,
            "month_maintenances": month_maintenances,
            "chart_data": chart_data,
        }

    except (ValueError, KeyError) as e:
        raise BusinessLogicError(f"Ошибка при расчете частоты обслуживания: {str(e)}")
