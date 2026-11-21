"""
ReminderService — логика напоминаний.

Единственная точка входа для cron: ReminderService.run_daily_check().
"""

from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo
from typing import Optional

from app.extensions import db
from app.models.maintenance import Maintenance, MaintenanceStatus
from app.models.motorcycle import Motorcycle
from app.models.reminder import Reminder
from app.models.user import User

# ============================================================
# КОНСТАНТЫ
# ============================================================

MILEAGE_STALE_DAYS = 30
MILEAGE_REPEAT_DAYS = 14
MAINTENANCE_SOON_THRESHOLD_KM = 500
MAINTENANCE_SOON_THRESHOLD_DAYS = 14
MAINTENANCE_OVERDUE_REPEAT_DAYS = 7


def _now() -> datetime:
    """Всегда UTC. Единая точка правды для тестов."""
    return datetime.now(timezone.utc)


def _today():
    """Календарная дата в часовом поясе приложения."""
    return _now().astimezone(ZoneInfo("Europe/Moscow")).date()


def _ensure_aware(dt: Optional[datetime]) -> Optional[datetime]:
    """
    Приводит любой datetime к aware UTC.
    None → None.
    """
    if dt is None:
        return None
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


class ReminderService:
    # ========================================================
    # ПУБЛИЧНЫЙ API — одна точка входа
    # ========================================================

    @staticmethod
    def run_daily_check() -> dict:
        """Синхронизирует актуальные напоминания и отправляет наступившие."""
        stats = {
            "created": 0,
            "sent": 0,
            "skipped": 0,
            "dismissed_auto": 0,
            "email_failed": 0,
            "no_permission": 0,
            "notifications_created": 0,
            "errors": 0,
        }

        try:
            sync_stats = ReminderService._sync_reminders()
            stats["created"] = sync_stats["created"]
            stats["dismissed_auto"] = sync_stats["dismissed_auto"]
        except Exception as error:
            db.session.rollback()
            print(f"[ReminderService] sync failed: {error}")
            stats["errors"] += 1
            return stats

        try:
            send_stats = ReminderService._send_due_reminders()
            for key in (
                "sent",
                "skipped",
                "email_failed",
                "no_permission",
                "notifications_created",
            ):
                stats[key] = send_stats.get(key, 0)
        except Exception as error:
            db.session.rollback()
            print(f"[ReminderService] send failed: {error}")
            stats["errors"] += 1

        return stats

    # ========================================================
    # ФАЗА 1: SYNC
    # ========================================================

    @staticmethod
    def _sync_reminders() -> dict:
        """Создаёт актуальные reminders и закрывает больше не нужные."""
        stats = {"created": 0, "dismissed_auto": 0}
        users = User.query.filter(User.status == "active").all()

        for user in users:
            if not user.reminders_mileage_enabled:
                stats["dismissed_auto"] += ReminderService._dismiss_pending(
                    user.id, [Reminder.TYPE_MILEAGE_UPDATE]
                )
            if not user.reminders_maintenance_enabled:
                stats["dismissed_auto"] += ReminderService._dismiss_pending(
                    user.id,
                    [
                        Reminder.TYPE_MAINTENANCE_SOON,
                        Reminder.TYPE_MAINTENANCE_OVERDUE,
                    ],
                )

            if not (
                user.reminders_mileage_enabled
                or user.reminders_maintenance_enabled
            ):
                continue

            motos = Motorcycle.query.filter_by(owner_id=user.id).all()
            for moto in motos:
                if user.reminders_mileage_enabled:
                    stats["created"] += ReminderService._ensure_mileage_reminder(
                        user, moto
                    )
                if user.reminders_maintenance_enabled:
                    created, dismissed = ReminderService._ensure_maintenance_reminders(
                        user, moto
                    )
                    stats["created"] += created
                    stats["dismissed_auto"] += dismissed

        db.session.commit()
        return stats

    @staticmethod
    def _dismiss_pending(user_id: int, reminder_types: list[str]) -> int:
        reminders = Reminder.query.filter(
            Reminder.user_id == user_id,
            Reminder.status == Reminder.STATUS_PENDING,
            Reminder.type.in_(reminder_types),
        ).all()
        for reminder in reminders:
            reminder.status = Reminder.STATUS_DISMISSED
            reminder.dismissed_at = _now()
            reminder.snoozed_until = None
        return len(reminders)

    @staticmethod
    def _ensure_mileage_reminder(user: User, moto: Motorcycle) -> int:
        """Создаёт reminder, если пробег мотоцикла давно не обновлялся."""
        last_touch = _ensure_aware(
            moto.mileage_updated_at or moto.updated_at or moto.created_at
        )
        if not last_touch:
            return 0

        if (_now() - last_touch).days < MILEAGE_STALE_DAYS:
            return 0

        existing = Reminder.query.filter_by(
            user_id=user.id,
            motorcycle_id=moto.id,
            type=Reminder.TYPE_MILEAGE_UPDATE,
            status=Reminder.STATUS_PENDING,
        ).first()
        if existing:
            return 0

        db.session.add(
            Reminder(
                user_id=user.id,
                motorcycle_id=moto.id,
                maintenance_id=None,
                type=Reminder.TYPE_MILEAGE_UPDATE,
                status=Reminder.STATUS_PENDING,
                next_send_at=None,
            )
        )
        return 1

    @staticmethod
    def _ensure_maintenance_reminders(user: User, moto: Motorcycle) -> tuple[int, int]:
        """
        Создаёт напоминания о ТО по пробегу и по плановой дате.
        ТО считается просроченным, если наступил любой из указанных сроков.
        """
        created = 0
        dismissed_auto = 0
        current_mileage = moto.mileage or 0
        today = _today()

        planned_maintenances = Maintenance.query.filter(
            Maintenance.moto_id == moto.id,
            Maintenance.status.in_(
                [MaintenanceStatus.PLANNED.value, MaintenanceStatus.OVERDUE.value]
            ),
        ).all()

        reminder_types = (
            Reminder.TYPE_MAINTENANCE_SOON,
            Reminder.TYPE_MAINTENANCE_OVERDUE,
        )
        existing = {
            (reminder.maintenance_id, reminder.type): reminder
            for reminder in Reminder.query.filter(
                Reminder.motorcycle_id == moto.id,
                Reminder.user_id == user.id,
                Reminder.status == Reminder.STATUS_PENDING,
                Reminder.type.in_(reminder_types),
            ).all()
        }
        active_keys = set()

        for maintenance in planned_maintenances:
            km_left = (
                maintenance.planned_mileage - current_mileage
                if maintenance.planned_mileage is not None
                else None
            )
            days_left = (
                (maintenance.planned_date - today).days
                if maintenance.planned_date is not None
                else None
            )
            has_schedule = km_left is not None or days_left is not None
            if not has_schedule:
                continue

            is_overdue = (
                maintenance.status == MaintenanceStatus.OVERDUE.value
                or (km_left is not None and km_left <= 0)
                or (days_left is not None and days_left <= 0)
            )
            is_soon = not is_overdue and (
                (
                    km_left is not None
                    and 0 < km_left <= MAINTENANCE_SOON_THRESHOLD_KM
                )
                or (
                    days_left is not None
                    and 0 < days_left <= MAINTENANCE_SOON_THRESHOLD_DAYS
                )
            )
            if not is_overdue and not is_soon:
                continue

            target_type = (
                Reminder.TYPE_MAINTENANCE_OVERDUE
                if is_overdue
                else Reminder.TYPE_MAINTENANCE_SOON
            )
            key = (maintenance.id, target_type)
            active_keys.add(key)

            opposite_type = (
                Reminder.TYPE_MAINTENANCE_SOON
                if is_overdue
                else Reminder.TYPE_MAINTENANCE_OVERDUE
            )
            opposite = existing.pop((maintenance.id, opposite_type), None)
            if opposite:
                opposite.status = Reminder.STATUS_DISMISSED
                opposite.dismissed_at = _now()
                opposite.snoozed_until = None
                dismissed_auto += 1

            if key not in existing:
                db.session.add(
                    Reminder(
                        user_id=user.id,
                        motorcycle_id=moto.id,
                        maintenance_id=maintenance.id,
                        type=target_type,
                        status=Reminder.STATUS_PENDING,
                    )
                )
                created += 1

        for key, reminder in existing.items():
            if key not in active_keys:
                reminder.status = Reminder.STATUS_DISMISSED
                reminder.dismissed_at = _now()
                reminder.snoozed_until = None
                dismissed_auto += 1

        return created, dismissed_auto

    # ========================================================
    # ФАЗА 2: SEND
    # ========================================================

    @staticmethod
    def _reminder_enabled(user: User, reminder_type: str) -> bool:
        if not user or user.status != "active":
            return False
        if reminder_type == Reminder.TYPE_MILEAGE_UPDATE:
            return bool(user.reminders_mileage_enabled)
        if reminder_type in (
            Reminder.TYPE_MAINTENANCE_SOON,
            Reminder.TYPE_MAINTENANCE_OVERDUE,
        ):
            return bool(user.reminders_maintenance_enabled)
        return False

    @staticmethod
    def _send_due_reminders() -> dict:
        from app.services.email_service import EmailService
        from app.services.notification_service import NotificationService

        stats = {
            "sent": 0,
            "skipped": 0,
            "email_failed": 0,
            "no_permission": 0,
            "notifications_created": 0,
        }

        now = _now()
        candidates = Reminder.query.filter(
            Reminder.status == Reminder.STATUS_PENDING,
        ).all()

        for reminder in candidates:
            if not ReminderService._should_send_now(reminder, now):
                stats["skipped"] += 1
                continue

            user = reminder.user
            if not user:
                stats["skipped"] += 1
                continue

            if not ReminderService._reminder_enabled(user, reminder.type):
                reminder.status = Reminder.STATUS_DISMISSED
                reminder.dismissed_at = now
                reminder.snoozed_until = None
                stats["skipped"] += 1
                continue

            try:
                (
                    notif_title,
                    notif_content,
                    notif_link,
                ) = ReminderService._build_notification_payload(reminder)
                NotificationService.send_notification(
                    user_id=user.id,
                    type="reminder",
                    title=notif_title,
                    content=notif_content,
                    link=notif_link,
                    extra_data={
                        "reminder_id": reminder.id,
                        "reminder_type": reminder.type,
                        "motorcycle_id": reminder.motorcycle_id,
                    },
                )
                stats["notifications_created"] += 1
            except Exception as e:
                print(
                    f"[ReminderService] Failed to create notification for reminder {reminder.id}: {e}"
                )

            if EmailService.can_send_reminder(user, reminder.type):
                ok = EmailService.send_reminder_email(user, reminder)
                if ok:
                    stats["sent"] += 1
                else:
                    stats["email_failed"] += 1
            else:
                stats["no_permission"] += 1

            reminder.last_sent_at = now
            reminder.next_send_at = ReminderService._compute_next_send(reminder, now)

        db.session.commit()
        return stats

    @staticmethod
    def _build_notification_payload(reminder: Reminder) -> tuple[str, str, str | None]:
        """Формирует текст in-app и push для конкретного напоминания."""
        moto = reminder.motorcycle
        moto_name = moto.name if moto else "мотоцикл"
        maintenance = reminder.maintenance

        if reminder.type == Reminder.TYPE_MILEAGE_UPDATE:
            current = moto.mileage if moto else 0
            return (
                f"🏍️ Обновите пробег для {moto_name}",
                f"Текущий пробег: {current} км. Свежие данные помогают точнее напоминать о ТО.",
                "/garage",
            )

        if reminder.type in (
            Reminder.TYPE_MAINTENANCE_SOON,
            Reminder.TYPE_MAINTENANCE_OVERDUE,
        ):
            is_overdue = reminder.type == Reminder.TYPE_MAINTENANCE_OVERDUE
            title_text = maintenance.title if maintenance else "обслуживание"
            title = (
                f"⚠️ Просрочено ТО: {title_text}"
                if is_overdue
                else f"🔧 Скоро ТО: {title_text}"
            )
            details = []
            current_mileage = moto.mileage or 0 if moto else 0

            if maintenance and maintenance.planned_mileage is not None:
                km_delta = maintenance.planned_mileage - current_mileage
                if km_delta > 0:
                    details.append(f"до планового пробега осталось примерно {km_delta} км")
                else:
                    details.append(f"просрочка по пробегу — {abs(km_delta)} км")

            if maintenance and maintenance.planned_date is not None:
                days_delta = (maintenance.planned_date - _today()).days
                planned_date = maintenance.planned_date.strftime("%d.%m.%Y")
                if days_delta > 0:
                    details.append(
                        f"плановая дата {planned_date}, осталось {days_delta} дн."
                    )
                else:
                    details.append(
                        f"плановая дата {planned_date}, срок прошёл {abs(days_delta)} дн. назад"
                    )

            if not details:
                details.append("откройте план обслуживания, чтобы посмотреть сроки")

            prefix = (
                f"Для {moto_name} просрочено обслуживание."
                if is_overdue
                else f"Для {moto_name} приближается обслуживание."
            )
            return title, f"{prefix} " + "; ".join(details) + ".", "/maintenance"

        return ("Напоминание", "У вас есть новое напоминание", "/garage")

    @staticmethod
    def _should_send_now(reminder: Reminder, now: datetime) -> bool:
        """
        Определяет, пора ли отправлять reminder.

        Логика:
        - Если snoozed_until > now → нет
        - Если next_send_at IS NULL → да (первый раз)
        - Если next_send_at <= now → да
        - Иначе → нет
        """
        if reminder.snoozed_until:
            snoozed = _ensure_aware(reminder.snoozed_until)
            if snoozed and snoozed > now:
                return False

        if reminder.next_send_at is None:
            return True

        next_send = _ensure_aware(reminder.next_send_at)
        return next_send <= now

    @staticmethod
    def _compute_next_send(reminder: Reminder, now: datetime) -> datetime:
        """Считает, когда слать следующий повтор."""
        if reminder.type == Reminder.TYPE_MILEAGE_UPDATE:
            return now + timedelta(days=MILEAGE_REPEAT_DAYS)
        if reminder.type == Reminder.TYPE_MAINTENANCE_OVERDUE:
            return now + timedelta(days=MAINTENANCE_OVERDUE_REPEAT_DAYS)
        return now + timedelta(days=3650)

    # ========================================================
    # ВСПОМОГАТЕЛЬНЫЕ
    # ========================================================

    @staticmethod
    def dismiss(reminder_id: int, user_id: int) -> Reminder:
        """Скрывает напоминание навсегда."""
        from app.exceptions import ForbiddenError, NotFoundError

        reminder = db.session.get(Reminder, reminder_id)
        if not reminder:
            raise NotFoundError("Напоминание не найдено")
        if reminder.user_id != user_id:
            raise ForbiddenError("Это не ваше напоминание")

        reminder.status = Reminder.STATUS_DISMISSED
        reminder.dismissed_at = _now()
        db.session.commit()
        return reminder

    @staticmethod
    def snooze(reminder_id: int, user_id: int, days: int = 7) -> Reminder:
        """Откладывает напоминание на N дней."""
        from app.exceptions import ForbiddenError, NotFoundError

        reminder = db.session.get(Reminder, reminder_id)
        if not reminder:
            raise NotFoundError("Напоминание не найдено")
        if reminder.user_id != user_id:
            raise ForbiddenError("Это не ваше напоминание")

        reminder.snoozed_until = _now() + timedelta(days=days)
        db.session.commit()
        return reminder

    @staticmethod
    def get_user_reminders(user_id: int, status: Optional[str] = None) -> list:
        """Возвращает reminders пользователя."""
        query = Reminder.query.filter_by(user_id=user_id)
        if status:
            query = query.filter_by(status=status)
        query = query.order_by(Reminder.created_at.desc())
        return query.all()

    @staticmethod
    def get_unread_count(user_id: int) -> int:
        """Счётчик для бейджа на колокольчике."""
        return Reminder.query.filter_by(
            user_id=user_id,
            status=Reminder.STATUS_PENDING,
        ).count()
