from datetime import datetime, timezone

from app.exceptions import NotFoundError, ValidationError
from app.extensions import db
from app.models.business_account import BusinessAccount
from app.models.business_client import BusinessClient


class BusinessClientService:
    """CRUD по клиентам бизнес-аккаунта."""

    @staticmethod
    def _get_account_for_user(user_id: int) -> BusinessAccount:
        account = BusinessAccount.query.filter_by(owner_id=user_id).first()
        if not account:
            raise NotFoundError("Бизнес-аккаунт не найден")
        return account

    @staticmethod
    def list_for_user(user_id: int, search: str = "") -> list[BusinessClient]:
        account = BusinessClientService._get_account_for_user(user_id)
        query = BusinessClient.query.filter_by(business_account_id=account.id)

        if search:
            q = f"{search.strip()}%"
            query = query.filter(
                db.or_(
                    BusinessClient.name.ilike(q),
                    BusinessClient.phone.ilike(q),
                    BusinessClient.email.ilike(q),
                )
            )

        return query.order_by(BusinessClient.created_at.desc()).all()

    @staticmethod
    def get_by_id(user_id: int, client_id: int) -> BusinessClient:
        account = BusinessClientService._get_account_for_user(user_id)
        client = db.session.get(BusinessClient, client_id)
        if not client or client.business_account_id != account.id:
            raise NotFoundError("Клиент не найден")
        return BusinessClient.query.filter_by(
            id=client_id,
            business_account_id=account.id,
        ).first()

    @staticmethod
    def create(user_id: int, **kwargs) -> BusinessClient:
        account = BusinessClientService._get_account_for_user(user_id)

        client = BusinessClient(
            business_account_id=account.id,
            name=kwargs.get("name"),
            phone=kwargs.get("phone"),
            email=kwargs.get("email"),
            note=kwargs.get("note"),
        )
        db.session.add(client)
        db.session.commit()
        return client

    @staticmethod
    def update(user_id: int, client_id: int, **updates) -> BusinessClient:
        client = BusinessClientService.get_by_id(user_id, client_id)

        for key, value in updates.items():
            if hasattr(client, key) and value is not None:
                setattr(client, key, value)

        db.session.commit()
        return client

    @staticmethod
    def delete(user_id: int, client_id: int) -> None:
        client = BusinessClientService.get_by_id(user_id, client_id)
        db.session.delete(client)
        db.session.commit()

    @staticmethod
    def link_to_user(user_id: int, client_id: int, email: str) -> BusinessClient:
        """
        Привязывает BusinessClient к реальному User по email.

        Правила:
        - email должен существовать среди зарегистрированных
        - клиент ещё не привязан
        - email должен совпадать с email пользователя
        """
        from app.models.user import User

        client = BusinessClientService.get_by_id(user_id, client_id)

        if client.user_id is not None:
            raise ValidationError("Клиент уже привязан к аккаунту")

        if not email or not email.strip():
            raise ValidationError("Укажите email")

        email = email.strip().lower()

        # Ищем пользователя
        target_user = User.query.filter(db.func.lower(User.email) == email).first()

        if not target_user:
            raise NotFoundError(
                "Пользователь с таким email не зарегистрирован в MotoBind"
            )

        account = BusinessClientService._get_account_for_user(user_id)
        duplicate = BusinessClient.query.filter(
            BusinessClient.business_account_id == account.id,
            BusinessClient.user_id == target_user.id,
            BusinessClient.id != client.id,
        ).first()

        if duplicate:
            raise ValidationError(
                f"Пользователь уже привязан к другому клиенту: «{duplicate.name}»"
            )

        client.user_id = target_user.id
        client.linked_at = datetime.now(timezone.utc)

        if not client.email:
            client.email = target_user.email

        db.session.commit()
        return client

    @staticmethod
    def unlink_from_user(user_id: int, client_id: int) -> BusinessClient:
        """Отвязывает клиента от реального User. Не удаляет клиента."""
        client = BusinessClientService.get_by_id(user_id, client_id)
        if client.user_id is None:
            raise ValidationError("Клиент не привязан")
        client.user_id = None
        client.linked_at = None
        db.session.commit()
        return client

    @staticmethod
    def list_for_client_user(client_user_id: int) -> list[BusinessClient]:
        """
        Возвращает всех BusinessClient, привязанных к реальному пользователю.

        Используется на стороне клиента — «Я клиент у мастеров».
        """
        return (
            BusinessClient.query.filter_by(user_id=client_user_id)
            .order_by(BusinessClient.linked_at.desc())
            .all()
        )
