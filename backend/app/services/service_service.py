from app.exceptions import NotFoundError, ValidationError
from app.extensions import db
from app.models.business_account import BusinessAccount
from app.models.service import Service, ServiceStatus
from app.services.business_service import BusinessAccountService


class ServiceService:
    """CRUD по услугам + модерация."""

    # ============================================================
    # ДЛЯ МАСТЕРА / СТО
    # ============================================================

    @staticmethod
    def list_for_user(user_id: int) -> list[Service]:
        account = BusinessAccountService.get_by_owner(user_id)
        return (
            Service.query.filter_by(business_account_id=account.id)
            .order_by(Service.created_at.desc())
            .all()
        )

    @staticmethod
    def get_for_user(user_id: int, service_id: int) -> Service:
        account = BusinessAccountService.get_by_owner(user_id)
        service = db.session.get(Service, service_id)
        if not service or service.business_account_id != account.id:
            raise NotFoundError("Услуга не найдена")
        return service

    @staticmethod
    def create(user_id: int, **kwargs) -> Service:
        account = BusinessAccountService.get_by_owner(user_id)

        ServiceService._validate_price_range(
            kwargs.get("price_from"),
            kwargs.get("price_to"),
        )

        service = Service(
            business_account_id=account.id,
            title=kwargs.get("title"),
            description=kwargs.get("description"),
            category=kwargs.get("category"),
            price_from=kwargs.get("price_from"),
            price_to=kwargs.get("price_to"),
            duration_min=kwargs.get("duration_min"),
            status=ServiceStatus.PENDING,
        )
        db.session.add(service)
        db.session.commit()
        return service

    @staticmethod
    def update(user_id: int, service_id: int, **updates) -> Service:
        service = ServiceService.get_for_user(user_id, service_id)

        if "price_from" in updates or "price_to" in updates:
            ServiceService._validate_price_range(
                updates.get("price_from", service.price_from),
                updates.get("price_to", service.price_to),
            )

        for key, value in updates.items():
            if hasattr(service, key) and value is not None:
                setattr(service, key, value)

        # Любое редактирование → снова на модерацию
        if service.status != ServiceStatus.PENDING:
            service.status = ServiceStatus.PENDING
            service.rejection_reason = None

        db.session.commit()
        return service

    @staticmethod
    def delete(user_id: int, service_id: int) -> None:
        service = ServiceService.get_for_user(user_id, service_id)
        db.session.delete(service)
        db.session.commit()

    # ============================================================
    # ПУБЛИЧНОЕ
    # ============================================================

    @staticmethod
    def list_public_for_slug(slug: str) -> list[Service]:
        account = BusinessAccountService.get_by_slug(slug)
        return (
            Service.query.filter_by(
                business_account_id=account.id,
                status=ServiceStatus.APPROVED,
            )
            .order_by(Service.created_at.desc())
            .all()
        )

    # ============================================================
    # АДМИН
    # ============================================================

    @staticmethod
    def list_for_admin(status: str | None = None, search: str = "") -> list[Service]:
        query = Service.query

        if status:
            query = query.filter_by(status=status)

        if search:
            q = f"%{search.strip()}%"
            query = query.filter(Service.title.ilike(q))

        return query.order_by(Service.created_at.desc()).all()

    @staticmethod
    def approve(service_id: int) -> Service:
        service = db.session.get(Service, service_id)
        if not service:
            raise NotFoundError("Услуга не найдена")
        if service.status == ServiceStatus.APPROVED:
            raise ValidationError("Услуга уже одобрена")

        service.status = ServiceStatus.APPROVED
        service.rejection_reason = None
        db.session.commit()
        return service

    @staticmethod
    def reject(service_id: int, reason: str) -> Service:
        service = db.session.get(Service, service_id)
        if not service:
            raise NotFoundError("Услуга не найдена")
        if service.status == ServiceStatus.REJECTED:
            raise ValidationError("Услуга уже отклонена")

        service.status = ServiceStatus.REJECTED
        service.rejection_reason = reason
        db.session.commit()
        return service

    # ============================================================
    # ХЕЛПЕРЫ
    # ============================================================

    @staticmethod
    def _validate_price_range(price_from, price_to):
        if price_from is not None and price_to is not None:
            if price_from > price_to:
                raise ValidationError("Цена «от» не может быть больше цены «до»")
