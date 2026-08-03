from typing import Optional

from flask_jwt_extended import get_jwt_identity

from app.exceptions import ForbiddenError, NotFoundError
from app.models.motorcycle import Motorcycle
from app.models.user import User


def get_current_user() -> User:
    """
    Получить текущего авторизованного пользователя
    Использовать только внутри эндпоинтов с @jwt_required
    """
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        raise NotFoundError("Пользователь не найден")
    return user


def get_current_user_id() -> int:
    """Получить ID текущего пользователя"""
    return int(get_jwt_identity())


def get_motorcycle_or_404(moto_id: int, user_id: Optional[int] = None) -> Motorcycle:
    """
    Получить мотоцикл по ID. Если передан user_id - проверяет владельца
    """
    moto = Motorcycle.query.get(moto_id)
    if not moto:
        raise NotFoundError("Мотоцикл не найден")

    if user_id and moto.owner_id != user_id:
        raise ForbiddenError("Вы не являетесь владельцем этого мотоцикла")

    return moto


def check_motorcycle_owner(moto_id: int, user_id: int) -> Motorcycle:
    """
    Проверить, что пользователь является владельцем мотоцикла.
    Возвращает мотоцикл, если проверка пройдена.
    """
    return get_motorcycle_or_404(moto_id, user_id)


def get_object_or_404(model, obj_id: int, error_message: str = "Объект не найден"):
    """
    Универсальная функция для получения объекта по ID или 404.
    """
    obj = model.query.get(obj_id)
    if not obj:
        raise NotFoundError(error_message)
    return obj
