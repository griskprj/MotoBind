from typing import Optional

from flask_jwt_extended import get_jwt_identity

from app.exceptions import ForbiddenError, NotFoundError
from app.extensions import db
from app.models.motorcycle import Motorcycle
from app.models.user import User


def get_current_user() -> User:
    """
    Получить текущего авторизованного пользователя
    Использовать только внутри эндпоинтов с @jwt_required
    """
    user_id = int(get_jwt_identity())
    user = db.session.get(User, user_id)
    if not user:
        raise NotFoundError("Пользователь не найден")
    return user


def get_current_user_id() -> int:
    """Получить ID текущего пользователя"""
    return int(get_jwt_identity())


def get_motorcycle_or_404(moto_id: int, user_id: Optional[int] = None) -> Motorcycle:
    """
    Получить мотоцикл по ID. Если передан user_id - проверяет владельца.
    """
    moto = db.session.get(Motorcycle, moto_id)
    if not moto:
        raise NotFoundError("Мотоцикл не найден")

    if user_id and moto.owner_id != user_id:
        raise ForbiddenError("Вы не являетесь владельцем этого мотоцикла")

    return moto


def get_object_or_404(model, obj_id: int, error_message: str = "Объект не найден"):
    """Универсальная функция для получения объекта по ID или 404."""
    obj = db.session.get(model, obj_id)
    if not obj:
        raise NotFoundError(error_message)
    return obj
