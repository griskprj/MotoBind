from typing import Optional

from app.models.user import User
from app.extensions import db
from app.exceptions import NotFoundError, ValidationError, ForbiddenError


class UserService:
    """ Сервис для работы с пользователями """
    
    @staticmethod
    def create_user(email: str, password: str, username: str, role: str) -> User:
        ''' Создает нового пользователя '''
        if User.query.filter_by(email=email).first():
            raise ValidationError("Пользователь с таким email уже существует")
        
        if User.query.filter_by(username=username).first():
            raise ValidationError("Имя пользователя занято")
        
        user = User(email=email, username=username, role=role, status='active')
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        return user
    
    @staticmethod
    def authenticate_user(email: str, password: str) -> User:
        """ Аутентифицирует пользователя """
        user = User.query.filter_by(email=email).first()
        if not user:
            raise NotFoundError("Пользователь с такой почтой не найден")
        if not user.check_password(password):
            raise ForbiddenError("Неверный пароль")
        
        return user
    
    @staticmethod
    def update_refresh_token(user: User, refresh_token: str) -> None:
        """ Обновляет refresh-токен пользователя """
        user.refresh_token = refresh_token
        db.session.commit()

    @staticmethod
    def clear_refresh_token(user: User) -> None:
        """ Очищает refresh-токен пользователя """
        user.refresh_token = None
        db.session.commit()

    @staticmethod
    def get_user_by_id(user_id: int) -> User:
        """ Получает пользователя по ID """
        user =  User.query.get(user_id)
        if not user:
            raise NotFoundError("Пользователь не найден")
        
    @staticmethod
    def get_user_by_email(email: str) -> Optional[User]:
        """ Получает пользователя по email """
        return User.query.filter_by(email=email).first()