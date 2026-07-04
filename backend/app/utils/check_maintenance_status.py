from datetime import datetime, timezone
from app.extensions import db


def check_status(maintenance, moto):
    """
    Вычисляет статус планового обслуживания на основе текущего пробега мотоцикла.
    Возвращает строку с статусом.
    """

    if not moto:
        raise ValueError("Мотоцикл не найден")
    if not maintenance:
        raise ValueError("Обслуживание не найдено")    
    
    if not maintenance.planned_mileage:
        return 'no_mileage'

    diff = maintenance.planned_mileage - moto.mileage

    if diff <= 0:
        return 'overdue'
    if 0 < diff <= 5000:
        return 'soon'
    else:
        return 'ok'
