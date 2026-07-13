from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt
from app.exceptions import ForbiddenError, UnauthorizedError

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
        role = claims.get('role')

        if role != 'admin':
            raise ForbiddenError("Доступ запрещен. Требуется роль администратора")
        
        return fn(*args, **kwargs)

    return wrapper