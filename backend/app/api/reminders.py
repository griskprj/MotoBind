from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.exceptions import ValidationError
from app.services.reminder_service import ReminderService
from app.models.reminder import Reminder
from app.schemas.reminder import SnoozeSchema

reminders_bp = Blueprint("reminders", __name__)


@reminders_bp.route("/", methods=["GET"])
@jwt_required()
def list_reminders():
    user_id = int(get_jwt_identity())
    status = request.args.get("status") or None

    if status and status not in (Reminder.STATUS_PENDING, Reminder.STATUS_DISMISSED):
        raise ValidationError("Недопустимый статус")

    items = ReminderService.get_user_reminders(user_id, status=status)

    return jsonify({
        "reminders": [r.to_dict(include_moto=True) for r in items],
        "total": len(items),
    }), 200


@reminders_bp.route("/count", methods=["GET"])
@jwt_required()
def unread_count():
    user_id = int(get_jwt_identity())
    count = ReminderService.get_unread_count(user_id)
    return jsonify({"count": count}), 200


@reminders_bp.route("/<int:reminder_id>/dismiss", methods=["PUT"])
@jwt_required()
def dismiss_reminder(reminder_id):
    user_id = int(get_jwt_identity())
    reminder = ReminderService.dismiss(reminder_id, user_id)
    return jsonify({
        "message": "Напоминание скрыто",
        "reminder": reminder.to_dict(),
    }), 200


@reminders_bp.route("/<int:reminder_id>/snooze", methods=["PUT"])
@jwt_required()
def snooze_reminder(reminder_id):
    user_id = int(get_jwt_identity())
    data = request.get_json() or {}
    schema = SnoozeSchema(**data)

    reminder = ReminderService.snooze(reminder_id, user_id, days=schema.days)
    return jsonify({
        "message": f"Напоминание отложено на {schema.days} дн.",
        "reminder": reminder.to_dict(),
    }), 200