"""
ReminderService — логика напоминаний.

Единственная точка входа для cron: ReminderService.run_daily_check().
"""

from datetime import datetime, timedelta, timezone
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
MAINTENANCE_OVERDUE_REPEAT_DAYS = 7


def _now() -> datetime:
    """Всегда UTC. Единая точка правды для тестов."""
    return datetime.now(timezone.utc)

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
        """
        Главный метод. Cron дёргает раз в сутки.

        Возвращает статистику для логов.
        """
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
            send_stats = ReminderService._send_due_reminders()
            stats["sent"] = send_stats["sent"]
            stats["skipped"] = send_stats["skipped"]
            stats["email_failed"] = send_stats.get("email_failed", 0)
            stats["no_permission"] = send_stats.get("no_permission", 0)
            stats["notifications_created"] = send_stats.get("notifications_created", 0)
        except Exception as e:
            db.session.rollback()
            print(f"[ReminderService] send failed: {e}")
            stats["errors"] += 1
            return stats

        try:
            send_stats = ReminderService._send_due_reminders()
            stats["sent"] = send_stats["sent"]
            stats["skipped"] = send_stats["skipped"]
        except Exception as e:
            db.session.rollback()
            print(f"[ReminderService] send failed: {e}")
            stats["errors"] += 1
            return stats

        return stats

    # ========================================================
    # ФАЗА 1: SYNC
    # ========================================================

    @staticmethod
    def _sync_reminders() -> dict:
        """
        Создаёт недостающие reminders и авто-dismiss'ит неактуальные.
        """
        stats = {"created": 0, "dismissed_auto": 0}

        users = User.query.filter(User.status == "active").all()

        for user in users:
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
    def _ensure_mileage_reminder(user: User, moto: Motorcycle) -> int:
        """
        Создаёт reminder типа 'mileage_update', если пробег устарел.
        Возвращает 1 если создан, иначе 0.
        """
        last_touch = _ensure_aware(
            moto.mileage_updated_at or moto.updated_at or moto.created_at
        )
        if not last_touch:
            return 0

        days_since = (_now() - last_touch).days

        days_since = (_now() - last_touch).days
        if days_since < MILEAGE_STALE_DAYS:
            return 0

        existing = Reminder.query.filter_by(
            user_id=user.id,
            motorcycle_id=moto.id,
            type=Reminder.TYPE_MILEAGE_UPDATE,
            status=Reminder.STATUS_PENDING,
        ).first()

        if existing:
            return 0

        reminder = Reminder(
            user_id=user.id,
            motorcycle_id=moto.id,
            maintenance_id=None,
            type=Reminder.TYPE_MILEAGE_UPDATE,
            status=Reminder.STATUS_PENDING,
            next_send_at=None,
        )
        db.session.add(reminder)
        return 1

    @staticmethod
    def _ensure_maintenance_reminders(user: User, moto: Motorcycle) -> tuple[int, int]:
        """
        Создаёт reminders для 'maintenance_soon' и 'maintenance_overdue'.
        Возвращает (created, dismissed_auto).

        Логика:
        - Для каждого planned ТО с planned_mileage:
            - если planned_mileage <= moto.mileage → overdue
            - elif planned_mileage - moto.mileage <= THRESHOLD → soon
        - Удаляем/дисмиссим reminders, для которых ТО стало completed/удалено
          или условия изменились (например, юзер откатил пробег).
        """
        created = 0
        dismissed_auto = 0

        current_mileage = moto.mileage or 0

        planned_maintenances = Maintenance.query.filter_by(
            moto_id=moto.id,
            status=MaintenanceStatus.PLANNED.value,
        ).all()

        existing = {
            (r.maintenance_id, r.type): r
            for r in Reminder.query.filter(
                Reminder.motorcycle_id == moto.id,
                Reminder.status == Reminder.STATUS_PENDING,
                Reminder.type.in_([
                    Reminder.TYPE_MAINTENANCE_SOON,
                    Reminder.TYPE_MAINTENANCE_OVERDUE,
                ]),
            ).all()
        }

        active_keys = set()

        for maint in planned_maintenances:
            if not maint.planned_mileage:
                continue

            km_left = maint.planned_mileage - current_mileage

            if km_left <= 0:
                key = (maint.id, Reminder.TYPE_MAINTENANCE_OVERDUE)
                active_keys.add(key)

                soon_key = (maint.id, Reminder.TYPE_MAINTENANCE_SOON)
                if soon_key in existing:
                    old = existing.pop(soon_key)
                    db.session.delete(old)
                    dismissed_auto += 1

                if key not in existing:
                    db.session.add(Reminder(
                        user_id=user.id,
                        motorcycle_id=moto.id,
                        maintenance_id=maint.id,
                        type=Reminder.TYPE_MAINTENANCE_OVERDUE,
                        status=Reminder.STATUS_PENDING,
                    ))
                    created += 1

            elif km_left <= MAINTENANCE_SOON_THRESHOLD_KM:
                key = (maint.id, Reminder.TYPE_MAINTENANCE_SOON)
                active_keys.add(key)

                if key not in existing:
                    db.session.add(Reminder(
                        user_id=user.id,
                        motorcycle_id=moto.id,
                        maintenance_id=maint.id,
                        type=Reminder.TYPE_MAINTENANCE_SOON,
                        status=Reminder.STATUS_PENDING,
                    ))
                    created += 1

        for key, reminder in existing.items():
            if key not in active_keys:
                db.session.delete(reminder)
                dismissed_auto += 1

        return created, dismissed_auto

    # ========================================================
    # ФАЗА 2: SEND
    # ========================================================

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

            try:
                notif_title, notif_content, notif_link = ReminderService._build_notification_payload(reminder)
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
                print(f"[ReminderService] Failed to create notification for reminder {reminder.id}: {e}")

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
        """
        Возвращает (title, content, link) для Notification
        в зависимости от типа reminder'а.
        """
        moto = reminder.motorcycle
        moto_name = moto.name if moto else "мотоцикл"

        if reminder.type == Reminder.TYPE_MILEAGE_UPDATE:
            current = moto.mileage if moto else 0
            return (
                f"🏍️ Обновите пробег для {moto_name}",
                f"Текущий пробег: {current} км. Свежие данные помогают точнее напоминать о ТО.",
                "/garage",
            )

        if reminder.type == Reminder.TYPE_MAINTENANCE_SOON:
            maint = reminder.maintenance
            title = f"🔧 Скоро ТО: {maint.title if maint else 'обслуживание'}"
            content = (
                f"Для {moto_name} приближается обслуживание. "
                f"План: {maint.planned_mileage if maint else '—'} км."
            )
            return title, content, "/maintenance"

        if reminder.type == Reminder.TYPE_MAINTENANCE_OVERDUE:
            maint = reminder.maintenance
            title = f"⚠️ Просрочено ТО: {maint.title if maint else 'обслуживание'}"
            content = (
                f"Для {moto_name} просрочено обслуживание. "
                f"План: {maint.planned_mileage if maint else '—'} км."
            )
            return title, content, "/maintenance"

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
        from app.exceptions import NotFoundError, ForbiddenError

        reminder = Reminder.query.get(reminder_id)
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
        from app.exceptions import NotFoundError, ForbiddenError

        reminder = Reminder.query.get(reminder_id)
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