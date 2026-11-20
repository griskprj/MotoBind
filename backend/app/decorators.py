from functools import wraps

from app.exceptions import ForbiddenError, NotFoundError, UnauthorizedError
from app.extensions import db
from app.models.business_account import BusinessAccount
from app.models.motorcycle import Motorcycle
from flask import g, jsonify
from flask_jwt_extended import get_jwt, get_jwt_identity, verify_jwt_in_request


def admin_required(fn):
    """
    Декоратор для проверки, что пользователь является администратором.
    Использовать вместе с jwt_required() или вместо него.
    """

    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()
        except Exception:
            raise UnauthorizedError("Отсутсвует или невалидный JWT-токен")

        claims = get_jwt()
        role = claims.get("role")

        if role != "admin":
            raise ForbiddenError("Доступ запрещен. Требуется роль администратора")

        return fn(*args, **kwargs)

    return wrapper


def owner_required(model, id_param_name="id", owner_field="owner_id"):
    """
    Декоратор для проверки, что пользователь явялется владельцем объекта.

    Использование:
        @owner_required(Motorcycle, 'moto_id')
        def update_moto(moto_id):
            ...

    Параметры:
        model: модель SQLAlchemy
        id_param_name: имя параметра в URL с ID объекта
        owner_field: имя поля в модели, хранящее ID владельца
    """

    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            try:
                verify_jwt_in_request()
            except Exception:
                raise UnauthorizedError("Отсутствует или невалидный JWT-токен")

            user_id = get_jwt_identity()
            obj_id = kwargs.get(id_param_name)

            if not obj_id:
                raise NotFoundError("ID объекта не указан")

            obj = model.query.get(obj_id)
            if not obj_id:
                raise NotFoundError(f"{model.__name__} не найден")

            owner_id = getattr(obj, owner_field)
            if int(owner_id) != int(user_id):
                raise ForbiddenError("Вы не являетесь владельцем этого объекта")

            return fn(*args, **kwargs)

        return wrapper

    return decorator


def moto_owner_required(fn):
    """
    Декоратор для проверки владельца мотоцикла.
    Ожидает параметр moto_id в URL.
    """

    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()
        except Exception:
            raise UnauthorizedError("Отсутствует или невалидный JWT-токен")

        user_id = get_jwt_identity()
        moto_id = kwargs.get("moto_id")

        if not moto_id:
            raise NotFoundError("ID мотоцикла не указан")

        moto = db.session.get(Motorcycle, moto_id)
        if not moto:
            raise NotFoundError("Мотоцикл не найден")

        if int(moto.owner_id) != int(user_id):
            raise ForbiddenError("Вы не являетесь владельцем этого мотоцикла")

        return fn(*args, **kwargs)

    return wrapper


def business_owner_required(fn):
    """
    Проверяет, что у текущего пользователя есть бизнес-аккаунт.
    Кладёт его в flask.g.business_account.

    Использование:
        @business_owner_required
        def my_endpoint():
            ba = g.business_account
            ...
    """

    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        user_id = int(get_jwt_identity())

        account = BusinessAccount.query.filter_by(owner_id=user_id).first()
        if not account:
            return jsonify({"error": "У вас нет бизнес-аккаунта. Создайте его."}), 403

        g.business_account = account
        return fn(*args, **kwargs)

    return wrapper
