from app.exceptions import BusinessLogicError
from app.utils.statistics_helpers import (
    aggregate_by_month,
    first_day_of_month,
    get_owned_motorcycle_or_403,
    is_in_month,
)


def _calculate_change_percent(current: float, previous: float) -> float:
    """Вычисляет процент изменения расходов."""
    if previous > 0:
        return round(((current - previous) / previous) * 100, 1)
    elif current > 0:
        return 100.0
    return 0.0


def calculate_maintenance_money(moto_id: int, user_id: int) -> dict:
    """
    Возвращает статистику затрат на обслуживание:
    - общие затраты
    - самое дорогое обслуживание
    - затраты в текущем месяце
    - средняя стоимость
    - данные для графика за 12 месяцев (по completed_date)
    """
    try:
        moto = get_owned_motorcycle_or_403(moto_id, user_id)
        maintenances = moto.maintenances

        completed = [m for m in maintenances if m.completed_date is not None]

        if not completed:
            return {
                "total_cost": 0,
                "max_cost": 0,
                "month_cost": 0,
                "average_cost": 0,
                "chart_data": [],
            }

        costs = [m.cost or 0 for m in completed]

        total_cost = sum(costs)
        max_cost = max(costs) if costs else 0
        average_cost = round(total_cost / len(completed), 2)

        month_start = first_day_of_month()
        month_cost = sum((m.cost or 0) for m in completed if is_in_month(m.completed_date, month_start))

        chart_data = aggregate_by_month(
            completed,
            date_getter=lambda m: m.completed_date,
            value_getter=lambda m: m.cost or 0,
        )

        return {
            "total_cost": total_cost,
            "max_cost": max_cost,
            "month_cost": month_cost,
            "average_cost": average_cost,
            "chart_data": chart_data,
        }

    except (ValueError, KeyError) as e:
        raise BusinessLogicError(f"Ошибка при расчете затрат: {str(e)}")
