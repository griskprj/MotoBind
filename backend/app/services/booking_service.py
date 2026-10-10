from datetime import datetime, timezone

from app.exceptions import ForbiddenError, NotFoundError, ValidationError
from app.extensions import db
from app.models.business_account import BusinessAccount
from app.models.motorcycle import Motorcycle
from app.models.service import Service, ServiceStatus
from app.models.service_booking import BookingStatus, ServiceBooking
from app.services.notification_service import NotificationService


class BookingService:
    """Логика заявок на обслуживание."""

    # ============================================================
    # СОЗДАНИЕ (КЛИЕНТ)
    # ============================================================

    @staticmethod
    def create(client_user_id: int, **kwargs) -> ServiceBooking:
        business = db.session.get(BusinessAccount, kwargs["business_account_id"])
        if not business:
            raise NotFoundError("Бизнес-аккаунт не найден")

        if business.owner_id == client_user_id:
            raise ValidationError("Нельзя записаться к самому себе")

        service = None
        if kwargs.get("service_id"):
            service = db.session.get(Service, kwargs["service_id"])
            if not service:
                raise NotFoundError("Услуга не найдена")
            if service.business_account_id != business.id:
                raise ValidationError("Услуга не принадлежит этому мастеру")
            if service.status != ServiceStatus.APPROVED:
                raise ValidationError("Услуга недоступна для записи")

        motorcycle = None
        if kwargs.get("motorcycle_id"):
            motorcycle = db.session.get(Motorcycle, kwargs["motorcycle_id"])
            if not motorcycle:
                raise NotFoundError("Мотоцикл не найден")
            if motorcycle.owner_id != client_user_id:
                raise ForbiddenError("Это не ваш мотоцикл")

        scheduled_at = BookingService._parse_datetime(kwargs["scheduled_at"])
        if scheduled_at < datetime.now(timezone.utc):
            raise ValidationError("Нельзя записаться на прошедшую дату")

        booking = ServiceBooking(
            client_user_id=client_user_id,
            business_account_id=business.id,
            service_id=service.id if service else None,
            motorcycle_id=motorcycle.id if motorcycle else None,
            scheduled_at=scheduled_at,
            client_note=kwargs.get("client_note"),
            status=BookingStatus.PENDING,
        )
        db.session.add(booking)
        db.session.commit()

        BookingService._notify(
            user_id=business.owner_id,
            title="Новая заявка",
            content=f"Запись на {scheduled_at.strftime('%d.%m.%Y %H:%M')}",
            link="/business/bookings",
            booking=booking,
        )

        return booking

    # ============================================================
    # ЧТЕНИЕ
    # ============================================================

    @staticmethod
    def get_for_client(client_user_id: int, booking_id: int) -> ServiceBooking:
        booking = db.session.get(ServiceBooking, booking_id)
        if not booking:
            raise NotFoundError("Заявка не найдена")
        if booking.client_user_id != client_user_id:
            raise ForbiddenError("Нет доступа")
        return booking

    @staticmethod
    def get_for_master(master_user_id: int, booking_id: int) -> ServiceBooking:
        booking = db.session.get(ServiceBooking, booking_id)
        if not booking:
            raise NotFoundError("Заявка не найдена")
        business = booking.business_account
        if not business or business.owner_id != master_user_id:
            raise ForbiddenError("Нет доступа")
        return booking

    @staticmethod
    def list_for_client(client_user_id: int, status: str | None = None):
        query = ServiceBooking.query.filter_by(client_user_id=client_user_id)
        if status:
            query = query.filter_by(status=status)
        return query.order_by(ServiceBooking.scheduled_at.desc()).all()

    @staticmethod
    def list_for_master(master_user_id: int, status: str | None = None):
        business = BusinessAccount.query.filter_by(owner_id=master_user_id).first()
        if not business:
            raise NotFoundError("Бизнес-аккаунт не найден")

        query = ServiceBooking.query.filter_by(business_account_id=business.id)
        if status:
            query = query.filter_by(status=status)

        if status in (None, "", BookingStatus.PENDING, BookingStatus.CONFIRMED):
            return query.order_by(ServiceBooking.scheduled_at.asc()).all()
        return query.order_by(ServiceBooking.scheduled_at.desc()).all()

    # ============================================================
    # ДЕЙСТВИЯ МАСТЕРА
    # ============================================================

    @staticmethod
    def confirm(master_user_id: int, booking_id: int) -> ServiceBooking:
        booking = BookingService.get_for_master(master_user_id, booking_id)
        BookingService._require_status(booking, BookingStatus.PENDING)

        booking.status = BookingStatus.CONFIRMED
        db.session.commit()

        BookingService._notify(
            user_id=booking.client_user_id,
            title="Заявка подтверждена",
            content=f"Мастер {booking.business_account.name} подтвердил вашу запись",
            link=f"/bookings/{booking.id}",
            booking=booking,
        )
        return booking

    @staticmethod
    def decline(
        master_user_id: int, booking_id: int, reason: str | None
    ) -> ServiceBooking:
        booking = BookingService.get_for_master(master_user_id, booking_id)
        BookingService._require_status(booking, BookingStatus.PENDING)

        booking.status = BookingStatus.DECLINED
        booking.cancel_reason = reason
        booking.cancelled_at = datetime.now(timezone.utc)
        db.session.commit()

        BookingService._notify(
            user_id=booking.client_user_id,
            title="Заявка отклонена",
            content=reason or "Мастер отклонил вашу запись",
            link=f"/bookings/{booking.id}",
            booking=booking,
        )
        return booking

    @staticmethod
    def reschedule(
        master_user_id: int, booking_id: int, scheduled_at: str
    ) -> ServiceBooking:
        booking = BookingService.get_for_master(master_user_id, booking_id)
        if booking.status not in (BookingStatus.PENDING, BookingStatus.CONFIRMED):
            raise ValidationError("Нельзя перенести в этом статусе")

        dt = BookingService._parse_datetime(scheduled_at)
        if dt < datetime.now(timezone.utc):
            raise ValidationError("Дата в прошлом")

        booking.scheduled_at = dt
        db.session.commit()

        BookingService._notify(
            user_id=booking.client_user_id,
            title="Запись перенесена",
            content=f"Новое время: {dt.strftime('%d.%m.%Y %H:%M')}",
            link=f"/bookings/{booking.id}",
            booking=booking,
        )
        return booking

    @staticmethod
    def start(master_user_id: int, booking_id: int) -> ServiceBooking:
        booking = BookingService.get_for_master(master_user_id, booking_id)
        BookingService._require_status(booking, BookingStatus.CONFIRMED)
        booking.status = BookingStatus.IN_PROGRESS
        db.session.commit()
        return booking

    @staticmethod
    def complete(
        master_user_id: int,
        booking_id: int,
        price_final: int | None,
        master_note: str | None,
    ) -> ServiceBooking:
        booking = BookingService.get_for_master(master_user_id, booking_id)
        if booking.status not in (BookingStatus.CONFIRMED, BookingStatus.IN_PROGRESS):
            raise ValidationError("Нельзя завершить в этом статусе")

        booking.status = BookingStatus.COMPLETED
        booking.completed_at = datetime.now(timezone.utc)
        booking.price_final = price_final
        if master_note is not None:
            booking.master_note = master_note

        db.session.commit()

        BookingService._notify(
            user_id=booking.client_user_id,
            title="Работа завершена",
            content=f"{booking.business_account.name} завершил работу",
            link=f"/bookings/{booking.id}",
            booking=booking,
        )
        return booking

    # ============================================================
    # ОТМЕНА (КЛИЕНТ)
    # ============================================================

    @staticmethod
    def cancel_by_client(
        client_user_id: int, booking_id: int, reason: str | None
    ) -> ServiceBooking:
        booking = BookingService.get_for_client(client_user_id, booking_id)
        if booking.status in (
            BookingStatus.COMPLETED,
            BookingStatus.CANCELLED,
            BookingStatus.DECLINED,
        ):
            raise ValidationError("Нельзя отменить в этом статусе")

        booking.status = BookingStatus.CANCELLED
        booking.cancel_reason = reason
        booking.cancelled_at = datetime.now(timezone.utc)
        db.session.commit()

        if booking.business_account:
            BookingService._notify(
                user_id=booking.business_account.owner_id,
                title="Клиент отменил заявку",
                content=reason or "Без указания причины",
                link="/business/bookings",
                booking=booking,
            )
        return booking

    # ============================================================
    # ХЕЛПЕРЫ
    # ============================================================

    @staticmethod
    def _parse_datetime(value: str) -> datetime:
        """Принимает ISO 8601 и приводит к UTC-aware datetime."""
        try:
            dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
        except (ValueError, AttributeError):
            raise ValidationError("Неверный формат даты. Используйте ISO 8601")

        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt

    @staticmethod
    def _require_status(booking: ServiceBooking, expected: str):
        if booking.status != expected:
            raise ValidationError(
                f"Ожидается статус «{expected}», текущий «{booking.status}»"
            )

    @staticmethod
    def _notify(user_id, title, content, link, booking):
        try:
            NotificationService.send_notification(
                user_id=user_id,
                type="booking",
                title=title,
                content=content,
                link=link,
                extra_data={"booking_id": booking.id},
            )
        except Exception:
            pass
