"""
Dev-планировщик для напоминаний.

Запускает run_daily_check раз в сутки в 9:00 МСК.
Работает ТОЛЬКО в dev-режиме (ENABLE_DEV_SCHEDULER=true).

В проде используйте системный cron (см. app/api/admin.py:cron_run_reminders).
"""

import os
from datetime import datetime, timedelta, timezone

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

_scheduler: BackgroundScheduler | None = None


def _run_job(app):
    """Обёртка, чтобы запускать в контексте приложения."""
    with app.app_context():
        from app.services.reminder_service import ReminderService

        try:
            stats = ReminderService.run_daily_check()
            app.logger.info(f"[Scheduler] run_daily_check: {stats}")
        except Exception:
            app.logger.exception("[Scheduler] run_daily_check failed")


def start_scheduler(app):
    """
    Запускает APScheduler в текущем процессе.
    Вызывается только из create_app при dev-режиме.
    """
    global _scheduler

    if os.environ.get("WERKZEUG_RUN_MAIN") != "true":
        app.logger.info("[Scheduler] WERKZEUG_RUN_MAIN != true — пропускаем (reloader)")
        return

    if app.config.get("DISABLE_SCHEDULER"):
        app.logger.info("[Scheduler] DISABLE_SCHEDULER=true — пропускаем")
        return

    if not app.config.get("ENABLE_DEV_SCHEDULER"):
        app.logger.info("[Scheduler] ENABLE_DEV_SCHEDULER=false — пропускаем")
        return

    if _scheduler is not None and _scheduler.running:
        app.logger.info("[Scheduler] уже запущен — пропускаем")
        return

    _scheduler = BackgroundScheduler(timezone="Europe/Moscow")

    _scheduler.add_job(
        func=_run_job,
        args=(app,),
        trigger=CronTrigger(hour=9, minute=0),
        id="daily_reminders",
        name="Daily reminders check",
        replace_existing=True,
        misfire_grace_time=3600,
    )

    _scheduler.start()
    app.logger.info("[Scheduler] APScheduler запущен, задача в 9:00 МСК")


def stop_scheduler():
    """Останавливает scheduler. Вызывается при завершении приложения."""
    global _scheduler
    if _scheduler and _scheduler.running:
        _scheduler.shutdown(wait=False)
        _scheduler = None