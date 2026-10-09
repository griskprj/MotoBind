from datetime import datetime, timezone

from app.exceptions import ForbiddenError, NotFoundError, ValidationError
from app.extensions import db
from app.models.business_account import BusinessAccount, BusinessType
from app.models.user import User
from app.utils.files import delete_file, save_business_logo
from app.utils.slugify import unique_slug


class BusinessAccountService:
    """Сервис бизнес-аккаунта (мастер или СТО)."""

    @staticmethod
    def create(user_id: int, **kwargs) -> BusinessAccount:
        """Создает бизнес-аккаунт. Один на пользователя."""
        existing = BusinessAccount.query.filter_by(owner_id=user_id).first()
        if existing:
            raise ValidationError("У вас уже есть бизнес-аккаунт")

        user = db.session.get(User, user_id)
        if not user:
            raise NotFoundError("Пользователь не найден")

        btype = kwargs.get("type")
        if btype not in (BusinessType.MASTER, BusinessType.STATION):
            raise ValidationError("Недопустимый тип аккаунта")

        name = kwargs.get("name")
        if not name:
            raise ValidationError("Название обязательно")

        slug = unique_slug(
            name,
            exists_fn=lambda s: BusinessAccount.query.filter_by(slug=s).first()
            is not None,
        )

        account = BusinessAccount(
            owner_id=user_id,
            name=name,
            slug=slug,
            description=kwargs.get("description"),
            city=kwargs.get("city"),
            address=kwargs.get("phone"),
            email=kwargs.get("email"),
            website=kwargs.get("website"),
        )

        db.session.add(account)
        db.session.commit()
        return account

    @staticmethod
    def get_by_owner(user_id: int) -> BusinessAccount:
        account = BusinessAccount.query.filter_by(owner_id=user_id).first()
        if not account:
            raise NotFoundError("Бизнес-аккаунт не найден")
        return account

    @staticmethod
    def get_by_slug(slug: str) -> BusinessAccount:
        account = BusinessAccount.query.filter_by(slug=slug).first()
        if not account:
            raise NotFoundError("Бизнес-аккаунт не найден")
        return account

    @staticmethod
    def update(user_id: int, **updates) -> BusinessAccount:
        account = BusinessAccountService.get_by_owner(user_id)

        name = updates.pop("name", None)
        if name and name != account.name:
            account.name = name
            account.slug = unique_slug(
                name,
                exists_fn=lambda s: BusinessAccount.query.filter(
                    BusinessAccount.slug == s,
                    BusinessAccount.id != account.id,
                ).first()
                is not None,
            )

        for key, value in updates.items():
            if hasattr(account, key) and value is not None:
                setattr(account, key, value)

        db.session.commit()
        return account

    @staticmethod
    def update_logo(user_id: int, file) -> BusinessAccount:
        """Загрузка логотипа. Тот же хелпер, что и для аватара."""
        account = BusinessAccountService.get_by_owner(user_id)

        if account.logo_url:
            delete_file(account.logo_url)

        path = save_business_logo(file, account.id)
        if not path:
            raise ValidationError(
                "Недопустимый формат файла. Разрешены: jpg, jpeg, png, gif, bmp, webp"
            )

        account.logo_url = path
        db.session.commit()
        return account

    @staticmethod
    def delete_logo(user_id: int) -> BusinessAccount:
        account = BusinessAccountService.get_by_owner(user_id)
        if account.logo_url:
            delete_file(account.logo_url)
            account.logo_url = None
            db.session.commit()

        return account
