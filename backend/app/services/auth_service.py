"""
AuthService — вся бизнес-логика аутентификации.

API-слой (app/api/auth.py) — тонкие контроллеры, вся работа с БД здесь.
"""
from datetime import datetime, timezone
from typing import Optional

from flask_jwt_extended import create_access_token, create_refresh_token

from app.exceptions import ForbiddenError, NotFoundError, UnauthorizedError, ValidationError
from app.extensions import db
from app.models.user import User
from app.services.user_service import UserService
from app.utils import email as email_utils


class AuthService:
    """Сервис аутентификации"""

    # ---- Registration / Login ----

    @staticmethod
    def register(
        email: str,
        password: str,
        username: str,
        role: str,
    ) -> dict:
        """
        Регистрирует пользователя, отправляет verify email,
        возвращает токены для автологина.

        Возвращает dict для ответа API (без response-схемы).
        """
        user = UserService.create_user(
            email=email,
            password=password,
            username=username,
            role=role,
        )

        email_utils.send_verification_email(user)

        access_token, refresh_token = AuthService._issue_tokens(user, remember_me=True)
        AuthService._save_refresh_token(user, refresh_token)

        return {
            "message": "Регистрация успешна! Подтвердите email.",
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": user.to_dict(),
            "requires_verification": True,
        }

    @staticmethod
    def login(email: str, password: str, remember_me: bool) -> dict:
        """
        Логин. Проверяет verified, banned, пароль.
        Возвращает токены.
        """
        user = UserService.authenticate_user(email=email, password=password)

        if not user.is_verified:
            raise ForbiddenError("Email не подтвержден. Проверьте почту")

        access_token, refresh_token = AuthService._issue_tokens(user, remember_me=remember_me)

        if remember_me:
            AuthService._save_refresh_token(user, refresh_token)
        else:
            refresh_token = None
            AuthService._clear_refresh_token(user)

        user.last_login = datetime.now(timezone.utc)
        db.session.commit()

        return {
            "message": "Вы вошли в аккаунт",
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": user.to_dict(),
        }

    # ---- Token refresh / logout ----

    @staticmethod
    def refresh(refresh_token: str) -> dict:
        """
        Обновляет access-токен по refresh-токену.

        Ротация refresh: старый становится невалидным.
        """
        if not refresh_token:
            raise ValidationError(
                "Refresh-токен обязателен",
                errors={"refresh_token": "Поле обязательно"},
            )

        user = User.query.filter_by(refresh_token=refresh_token).first()
        if not user:
            raise UnauthorizedError("Невалидный refresh-токен")

        access_token = create_access_token(
            identity=str(user.id),
            additional_claims={"role": user.role},
        )
        new_refresh_token = create_refresh_token(identity=str(user.id))

        user.refresh_token = new_refresh_token
        db.session.commit()

        return {
            "access_token": access_token,
            "refresh_token": new_refresh_token,
        }

    @staticmethod
    def logout(user: User) -> None:
        """Очищает refresh_token пользователя."""
        user.refresh_token = None
        db.session.commit()

    # ---- Email verification ----

    @staticmethod
    def send_verification(user: User) -> str:
        """
        Отправляет письмо для подтверждения email.

        Возвращает сообщение для ответа API.
        Если email уже подтверждён — вернёт соответствующее сообщение (без отправки).
        """
        if user.is_verified:
            return "Email уже подтвержден"

        email_utils.send_verification_email(user)
        return "Письмо отправлено"

    @staticmethod
    def verify_email(token: str) -> dict:
        """
        Подтверждает email по токену из письма.
        Генерирует токены для автоматического входа.
        """
        email = email_utils.verify_token(token)
        if not email:
            raise ValidationError("Ссылка недействительна или истекла")

        user = User.query.filter_by(email=email).first()
        if not user:
            raise NotFoundError("Пользователь не найден")

        if user.is_verified:
            return {"message": "Email уже подтвержден"}

        user.is_verified = True
        db.session.commit()

        access_token, refresh_token = AuthService._issue_tokens(user, remember_me=True)

        return {
            "message": "Email подтвержден!",
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": user.to_dict(),
        }

    # ---- Password reset ----

    @staticmethod
    def forgot_password(email: Optional[str]) -> None:
        """
        Отправляет письмо для сброса пароля, если email существует.

        Не раскрывает существование email — всегда "ok".
        """
        if not email:
            raise ValidationError("Email обязателен")

        user = User.query.filter_by(email=email).first()
        if user:
            email_utils.send_reset_email(user)

    @staticmethod
    def reset_password(token: Optional[str], new_password: Optional[str]) -> None:
        """
        Меняет пароль по токену из письма.
        """
        if not token or not new_password:
            raise ValidationError("Токен и новый пароль обязательны")

        if len(new_password) < 6:
            raise ValidationError("Пароль должен быть минимум 6 символов")

        email = email_utils.verify_reset_token(token)
        if not email:
            raise ValidationError("Ссылка недействительна или истекла")

        user = User.query.filter_by(email=email).first()
        if not user:
            raise NotFoundError("Пользователь не найден")

        user.set_password(new_password)
        db.session.commit()

    @staticmethod
    def check_reset_token(token: str) -> str:
        """Возвращает email, если токен валиден. Иначе — ValidationError."""
        email = email_utils.verify_reset_token(token)
        if not email:
            raise ValidationError("Ссылка недействительна или истекла")
        return email

    # ---- Private helpers ----

    @staticmethod
    def _issue_tokens(user: User, remember_me: bool) -> tuple[str, Optional[str]]:
        """
        Генерирует access (+ refresh, если remember_me) токены.

        Returns (access_token, refresh_token_or_none).
        """
        access_token = create_access_token(
            identity=str(user.id),
            additional_claims={"role": user.role},
        )
        if not remember_me:
            return access_token, None
        refresh_token = create_refresh_token(identity=str(user.id))
        return access_token, refresh_token

    @staticmethod
    def _save_refresh_token(user: User, refresh_token: Optional[str]) -> None:
        if refresh_token is None:
            return
        user.refresh_token = refresh_token
        db.session.commit()

    @staticmethod
    def _clear_refresh_token(user: User) -> None:
        if user.refresh_token is not None:
            user.refresh_token = None
            db.session.commit()