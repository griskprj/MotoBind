"""
Общие helpers для расчета статистики по обслуживанию.
"""
from datetime import date, datetime
from typing import Callable, Iterable, List, Optional

from app.exceptions import ForbiddenError, NotFoundError
from app.extensions import db
from app.models.motorcycle import Motorcycle
from app.models.user import User


def get_owned_motorcycle_or_403(moto_id: int, user_id: int) -> Motorcycle:
    """
    Загружает мотоцикл с предзагрузкой ТО и проверяет владельца (или admin).
    Используется в аналитических функциях статистики.
    """
    user = db.session.get(User, user_id)
    if not user:
        raise NotFoundError("Пользователь не найден")

    moto = db.session.get(Motorcycle, moto_id)
    if not moto:
        raise NotFoundError("Мотоцикл не найден")

    if int(moto.owner_id) != int(user.id) and user.role != "admin":
        raise ForbiddenError("Вы не являетесь владельцем этого мотоцикла")

    return moto

def iter_last_12_months(today: Optional[date] = None) -> List[date]:
    """
    Возвращает список из 12 первых дней месяцев,
    от 11 месяцев назад до текущего включительно (по возрастанию).
    Пример для 2026-09-15: ['2025-10-01', ..., '2026-09-01'].
    """
    today = today or date.today()
    months = []
    year, month = today.year, today.month
    for _ in range(12):
        months.append(date(year, month, 1))
        month -= 1
        if month == 0:
            month = 12
            year -= 1
    return list(reversed(months))

def month_bounds(month_start: date) -> tuple[date, date]:
    """Возвращает (первый день, первый день следующего месяца)."""
    if month_start.month == 12:
        next_month = date(month_start.year + 1, 1, 1)
    else:
        next_month = date(month_start.year, month_start.month + 1, 1)
    return month_start, next_month

def aggregate_by_month(
    maintenances: Iterable,
    date_getter: Callable,
    value_getter: Callable,
    today: Optional[date] = None,
) -> List[dict]:
    """
    Группирует значения по месяцам за последние 12 месяцев.
    - date_getter(m) -> date | None (для фильтра)
    - value_getter(m) -> number (слагаемое или 1)
    
    Возвращает [{"month": "2026-09", "value": N}, ...] - 12 точек по возрастанию.
    """
    today = today or date.today()
    result = []
    for month_start in iter_last_12_months(today):
        _, next_month = month_bounds(month_start)
        total = 0
        for m in maintenances:
            d = date_getter(m)
            if d is None:
                continue

            if isinstance(d, datetime):
                d = d.date()
            if month_start <= d < next_month:
                total += value_getter(m)
        result.append({
            "month": month_start.strftime("%Y-%m"),
            "value": total,
        })
    return result

def is_in_month(d: Optional[date], month_start: date) -> bool:
    """Проверяет, попадает ли дата в указанный месяц."""
    if d is None:
        return False
    if isinstance(d, datetime):
        d = d.date()
    _, next_month = month_bounds(month_start)
    return month_start <= d < next_month

def first_day_of_month(d: Optional[date] = None) -> date:
    """Первый день текущего месяца."""
    d = d or date.today()
    return date(d.year, d.month, 1)