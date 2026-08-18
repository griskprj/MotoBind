from typing import Optional
from datetime import datetime, timezone, timedelta
from app.exceptions import ForbiddenError, NotFoundError, ValidationError
from app.extensions import db
from app.models.user import User
from app.utils.files import delete_file, save_user_avatar
from app.services.email_service import EmailService


class UserService:
    """Сервис для работы с пользователями"""

    @staticmethod
    def create_user(email: str, password: str, username: str, role: str) -> User:
        """Создает нового пользователя"""
        if User.query.filter_by(email=email).first():
            raise ValidationError("Пользователь с таким email уже существует")

        if User.query.filter_by(username=username).first():
            raise ValidationError("Имя пользователя занято")

        user = User(
            email=email, 
            username=username, 
            role=role, 
            status="active", 
            is_verified=False
        )
        user.set_password(password)

        code = EmailService.generate_verification_code()
        user.verification_code = code
        user.verification_code_expires = datetime.now(timezone.utc) + timedelta(minutes=15)


        db.session.add(user)
        db.session.commit()

        EmailService.send_verification_email(email, code)

        return user

    @staticmethod
    def verify_email(email: str, code: str) -> User:
        """Подтверждение email по коду"""
        user = User.query.filter_by(email=email).first()
        if not user:
            raise ValidationError("Пользователь не найден")
        
        if user.is_verified:
            raise ValidationError("Email уже подтвержден")
        
        if user.verification_code != code:
            raise ValidationError("Неверный код подтверждения")
        
        if user.verification_code_expires < datetime.now(timezone.utc):
            raise ValidationError("Код подтверждения истек. Запросите новый")
        
        user.is_verified = True
        user.verification_code = None
        user.verification_code_expires = None
        db.session.commit()
        
        return user
    
    @staticmethod
    def resend_verification_code(email: str) -> dict:
        """Отправка нового кода подтверждения"""
        user = User.query.filter_by(email=email).first()
        if not user:
            raise ValidationError("Пользователь не найден")
        
        if user.is_verified:
            raise ValidationError("Email уже подтвержден")
        
        code = EmailService.generate_verification_code()
        user.verification_code = code
        user.verification_code_expires = datetime.now(timezone.utc) + timedelta(minutes=15)
        db.session.commit()
        
        EmailService.send_verification_email(email, code)
        
        return {"message": "Новый код отправлен на email"}
    
    @staticmethod
    def request_password_reset(email: str) -> dict:
        """Запрос на сброс пароля"""
        user = User.query.filter_by(email=email).first()
        if not user:
            raise ValidationError("Пользователь с таким email не найден")
        
        code = EmailService.generate_verification_code()
        user.reset_password_code = code
        user.reset_password_expires = datetime.now(timezone.utc) + timedelta(minutes=15)
        db.session.commit()
        
        EmailService.send_password_reset_email(email, code)
        
        return {"message": "Код для сброса пароля отправлен на email"}
    
    @staticmethod
    def reset_password(email: str, code: str, new_password: str) -> User:
        """Сброс пароля по коду"""
        user = User.query.filter_by(email=email).first()
        if not user:
            raise ValidationError("Пользователь не найден")
        
        if user.reset_password_code != code:
            raise ValidationError("Неверный код")
        
        if user.reset_password_expires < datetime.now(timezone.utc):
            raise ValidationError("Код истек. Запросите новый")
        
        user.set_password(new_password)
        user.reset_password_code = None
        user.reset_password_expires = None
        db.session.commit()
        
        return user

    @staticmethod
    def authenticate_user(email: str, password: str) -> User:
        """Аутентифицирует пользователя"""
        user = User.query.filter_by(email=email).first()
        if not user:
            raise NotFoundError("Пользователь с такой почтой не найден")
        if user.status == "banned":
            raise ForbiddenError("Вы были заблокированы")
        if not user.check_password(password):
            raise ForbiddenError("Неверный пароль")

        return user

    @staticmethod
    def update_profile(user_id: int, **kwargs) -> User:
        """Обновляет данные профиля"""
        user = UserService.get_user_by_id(user_id)
        for key, value in kwargs.items():
            if hasattr(user, key) and value is not None:
                setattr(user, key, value)
        db.session.commit()
        return user

    @staticmethod
    def update_avatar(user_id: int, file) -> User:
        """Обновляет аватар пользователя"""
        user = UserService.get_user_by_id(user_id)
        
        # Удаляем старый аватар, если есть
        if user.avatar:
            delete_file(user.avatar)
        
        # Сохраняем новый аватар
        avatar_path = save_user_avatar(file, user_id)
        if not avatar_path:
            raise ValidationError("Недопустимый формат файла. Разрешены: jpg, jpeg, png, gif, bmp, webp")
        
        user.avatar = avatar_path
        db.session.commit()
        
        return user

    @staticmethod
    def delete_avatar(user_id: int) -> User:
        """Удаляет аватар пользователя"""
        user = UserService.get_user_by_id(user_id)
        
        if user.avatar:
            delete_file(user.avatar)
            user.avatar = None
            db.session.commit()
        
        return user

    @staticmethod
    def change_password(user_id: int, current_password: str, new_password: str) -> User:
        """Обновляет пароль"""
        user = UserService.get_user_by_id(user_id)
        if not user.check_password(current_password):
            raise ForbiddenError("Неверный текущий пароль")
        user.set_password(new_password)
        db.session.commit()
        return user

    @staticmethod
    def delete_account(user_id: int, password: str) -> None:
        """Удаляет аккаунт"""
        user = UserService.get_user_by_id(user_id)
        if not user.check_password(password):
            raise ForbiddenError("Неверный пароль")
        db.session.commit()

    @staticmethod
    def update_refresh_token(user: User, refresh_token: str) -> None:
        """Обновляет refresh-токен пользователя"""
        user.refresh_token = refresh_token
        db.session.commit()

    @staticmethod
    def clear_refresh_token(user: User) -> None:
        """Очищает refresh-токен пользователя"""
        user.refresh_token = None
        db.session.commit()

    @staticmethod
    def get_user_by_id(user_id: int) -> User:
        """Получает пользователя по ID"""
        user = User.query.get(user_id)
        if not user:
            raise NotFoundError("Пользователь не найден")

        return user

    @staticmethod
    def get_user_by_email(email: str) -> Optional[User]:
        """Получает пользователя по email"""
        return User.query.filter_by(email=email).first()