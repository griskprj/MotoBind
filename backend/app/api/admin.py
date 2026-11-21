from datetime import datetime, timezone

from app.decorators import admin_required
from app.exceptions import ConflictError, NotFoundError, ValidationError
from app.extensions import db
from app.models.manual import Manual
from app.models.motorcycle import Motorcycle
from app.models.post_report import PostReport
from app.models.slot_adjustment import SlotAdjustment
from app.models.slot_purchase import SlotPurchase
from app.models.user import User
from app.schemas.admin import CreateUserSchema, UpdateUserSchema
from app.schemas.service import RejectServiceSchema
from app.services.admin_service import AdminService
from app.services.email_service import EmailService
from app.services.notification_service import NotificationService
from app.services.reminder_service import ReminderService
from app.services.report_service import ReportService
from app.services.service_service import ServiceService
from flask import Blueprint, current_app, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from sqlalchemy import String, cast, desc, func, or_

admin = Blueprint("admin", __name__)


@admin.route("/slot-purchases", methods=["GET"])
@jwt_required()
@admin_required
def list_slot_purchases():
    page = max(1, request.args.get("page", 1, type=int))
    per_page = min(100, max(1, request.args.get("per_page", 20, type=int)))
    status = request.args.get("status") or None
    search = (request.args.get("search") or "").strip()
    query = SlotPurchase.query.join(User, SlotPurchase.user_id == User.id)
    if status in {"pending", "paid", "refunded"}:
        query = query.filter(SlotPurchase.status == status)
    if search:
        query = query.filter(or_(
            User.email.ilike(f"%{search}%"),
            User.username.ilike(f"%{search}%"),
            cast(SlotPurchase.id, String).ilike(f"%{search}%"),
        ))
    purchases = query.order_by(SlotPurchase.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)
    adjustments = SlotAdjustment.query.order_by(SlotAdjustment.created_at.desc()).limit(100).all()
    return jsonify({
        "purchases": [purchase.to_admin_dict() for purchase in purchases.items],
        "adjustments": [item.to_dict() for item in adjustments],
        "total": purchases.total,
        "pages": purchases.pages,
        "current_page": purchases.page,
        "per_page": purchases.per_page,
    }), 200


@admin.route("/slot-purchases/gift", methods=["POST"])
@jwt_required()
@admin_required
def gift_motorcycle_slots():
    data = request.get_json(silent=True) or {}
    email = str(data.get("email", "")).strip().lower()
    reason = str(data.get("reason", "")).strip()
    quantity = data.get("quantity", 1)
    if not email or not reason:
        raise ValidationError("Email пользователя и причина обязательны")
    if not isinstance(quantity, int) or isinstance(quantity, bool) or quantity < 1 or quantity > 20:
        raise ValidationError("Количество мест должно быть от 1 до 20")
    if len(reason) > 500:
        raise ValidationError("Причина не должна превышать 500 символов")
    user = User.query.filter(func.lower(User.email) == email).first()
    if user is None:
        raise NotFoundError("Пользователь с таким email не найден")
    admin_user = db.session.get(User, int(get_jwt_identity()))
    adjustment = SlotAdjustment(
        user_id=user.id,
        user_email=user.email,
        admin_id=admin_user.id,
        admin_email=admin_user.email,
        quantity=quantity,
        reason=reason,
    )
    db.session.add(adjustment)
    db.session.commit()
    return jsonify({"message": "Подарочные места выданы", "adjustment": adjustment.to_dict()}), 201


@admin.route("/slot-purchases/<int:purchase_id>/refund", methods=["POST"])
@jwt_required()
@admin_required
def record_slot_refund(purchase_id):
    data = request.get_json(silent=True) or {}
    reason = str(data.get("reason", "")).strip()
    reference = str(data.get("reference", "")).strip() or None
    if not reason:
        raise ValidationError("Укажите причину возврата")
    if len(reason) > 500 or (reference and len(reference) > 128):
        raise ValidationError("Слишком длинная причина или номер операции")
    purchase = SlotPurchase.query.filter_by(id=purchase_id).with_for_update().first()
    if purchase is None:
        raise NotFoundError("Покупка не найдена")
    if purchase.status != "paid":
        raise ConflictError("Возврат можно отметить только для оплаченной покупки")
    purchase.status = "refunded"
    purchase.refunded_at = datetime.now(timezone.utc)
    purchase.refund_reason = reason
    purchase.refund_reference = reference
    purchase.refunded_by = int(get_jwt_identity())
    admin_user = db.session.get(User, purchase.refunded_by)
    purchase.refunded_by_email = admin_user.email if admin_user else ""
    db.session.commit()
    return jsonify({"message": "Возврат отмечен", "purchase": purchase.to_admin_dict()}), 200


@admin.route("/get", methods=["GET"])
@jwt_required()
@admin_required
def get_dashboard_data():
    """
    Получение данных админ-панели
    """

    users = User.query.all()
    users_count = 0
    users_data = []
    for user in users:
        users_data.append(user.to_dict(include_moto=True))
        users_count += 1

    manuals = Manual.query.all()
    manuals_count = 0
    manuals_data = []
    for manual in manuals:
        manuals_count += 1
        manuals_data.append(manual.to_dict())

    motorcycles_count = len([m for m in Motorcycle.query.all()])

    return (
        jsonify(
            {
                "users": users_data,
                "manuals": manuals_data,
                "users_count": users_count,
                "manuals_count": manuals_count,
                "motorcycles_count": motorcycles_count,
            }
        ),
        200,
    )


@admin.route("/users", methods=["GET"])
@jwt_required()
@admin_required
def get_users():
    """
    Получение пользователей
    """
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    search = request.args.get("search", "")
    role = request.args.get("role", "")
    status = request.args.get("status")
    date_from = request.args.get("date_from", "")
    date_to = request.args.get("date_to", "")

    query = User.query

    if search:
        query = query.filter(
            or_(
                User.username.ilike(f"%{search}"),
                User.email.ilike(f"%{search}"),
                User.id.ilike(f"%{search}"),
            )
        )

    if role:
        query = query.filter(User.role == role)
    if status:
        query = query.filter(User.status == status)
    if date_from:
        query = query.filter(User.created_at >= date_from)
    if date_to:
        query = query.filter(User.created_at <= date_to)

    sort_by = request.args.get("sort_by", "created_at")
    sort_order = request.args.get("sort_order", "desc")

    if sort_order == "desc":
        query = query.order_by(desc(getattr(User, sort_by, User.created_at)))
    else:
        query = query.order_by(getattr(User, sort_by, User.created_at))

    paginated = query.paginate(page=page, per_page=per_page, error_out=False)

    total_users = User.query.count()
    active_users = User.query.filter(User.status == "active").count()
    block_users = User.query.filter(User.status == "banned").count()
    admin_users = User.query.filter(User.role == "admin").count()

    return jsonify(
        {
            "users": [user.to_dict() for user in paginated.items],
            "total": paginated.total,
            "pages": paginated.pages,
            "current_page": paginated.page,
            "per_page": paginated.per_page,
            "has_prev": paginated.has_prev,
            "has_next": paginated.has_next,
            "stats": {
                "total": total_users,
                "active": active_users,
                "banned": block_users,
                "admin": admin_users,
            },
        }
    )


@admin.route("/manual/<int:manual_id>/approve", methods=["POST"])
@jwt_required()
@admin_required
def approve_manual(manual_id):
    """
    Одобрение мануала
    """
    manual = db.session.get(Manual, manual_id)
    if not manual:
        raise NotFoundError("Мануал не найден")

    if manual.status != "moderate":
        raise ValidationError(f"Мануал уже обработан (статус: {manual.status})")

    manual.status = "approved"
    db.session.commit()

    NotificationService.send_notification(
        user_id=manual.author_id,
        type="manual_status",
        title="Мануал одобрен",
        content=f'Ваш мануал "{manual.title}" был одобрен и опубликован.',
        link=f"/manual/{manual.id}",
        extra_data={"manual_id": manual.id, "status": "approved"},
    )

    return (
        jsonify({"message": "Мануал успешно одобрен", "manual": manual.to_dict()}),
        200,
    )


@admin.route("/manual/<int:manual_id>/reject", methods=["POST"])
@jwt_required()
@admin_required
def reject_manual(manual_id):
    """
    Отклонение мануала
    """

    manual = db.session.get(Manual, manual_id)
    if not manual:
        raise NotFoundError("Мануал не найден")

    if manual.status != "moderate":
        raise ValidationError(f"Мануал уже обработан (статус: {manual.status})")

    data = request.get_json(silent=True)
    if not data:
        raise ValidationError("Нет данных")

    reason = data.get("reason", "Без указания причины")

    manual.status = "rejected"
    manual.rejection_reason = reason

    db.session.commit()

    NotificationService.send_notification(
        user_id=manual.author_id,
        type="manual_status",
        title="Мануал отклонен",
        content=f'Ваш мануал "{manual.title}" был отклонен. Причина: {reason}',
        link=f"/manual/{manual.id}",
        extra_data={"manual_id": manual.id, "status": "rejected", "reason": reason},
    )

    return jsonify({"message": "Мануал отклонен", "manual": manual.to_dict()}), 200


@admin.route("/manual/<int:manual_id>/reconsider", methods=["POST"])
@jwt_required()
@admin_required
def reconsider_manual(manual_id):
    """
    Пересмотр мануала
    """

    manual = db.session.get(Manual, manual_id)
    if not manual:
        raise NotFoundError("Мануал не найден")

    if manual.status == "moderate":
        raise ValidationError("Мануал уже на проверке")

    manual.status = "moderate"
    manual.rejection_reason = None
    db.session.commit()

    NotificationService.send_notification(
        user_id=manual.author_id,
        type="manual_status",
        title="Мануал отправлен на повторную проверку",
        content=f'Ваш мануал "{manual.title}" отправлен на повторную проверку.',
        link=f"/manual/{manual.id}",
        extra_data={"manual_id": manual.id, "status": "moderate"},
    )

    return (
        jsonify(
            {"message": "Мануал возвращен на проверку", "manual": manual.to_dict()}
        ),
        200,
    )


@admin.route("/manual/<int:manual_id>", methods=["DELETE"])
@jwt_required()
@admin_required
def delete_manual(manual_id):
    """
    Удаление мануала
    """

    manual = db.session.get(Manual, manual_id)
    if not manual:
        raise NotFoundError("Мануал не найден")

    db.session.delete(manual)
    db.session.commit()

    return (
        jsonify(
            {
                "message": "Мануал удален",
            }
        ),
        200,
    )


@admin.route("/user", methods=["POST"])
@jwt_required()
@admin_required
def create_user():
    """
    Создание пользователя
    """
    data = CreateUserSchema(**request.get_json(silent=True))
    user = AdminService.create_user(
        email=data.email,
        username=data.username,
        role=data.role,
        status=data.status,
        password=data.password,
    )
    return jsonify(user.to_dict()), 201


@admin.route("/user/<int:user_id>/ban", methods=["POST"])
@jwt_required()
@admin_required
def ban_user(user_id):
    """
    Блокировка пользователя
    """

    user = db.session.get(User, user_id)
    if not user:
        raise NotFoundError("Пользователь не найден")

    current_user_id = int(get_jwt_identity())
    if int(user.id) == current_user_id:
        raise ValidationError("Нельзя заблокировать самого себя")

    user.status = "banned"
    db.session.commit()

    return (
        jsonify(
            {
                "message": f"Пользователь {user.username} заблокирован",
                "user": user.to_dict(),
            }
        ),
        200,
    )


@admin.route("/user/<int:user_id>/unban", methods=["POST"])
@jwt_required()
@admin_required
def unban_user(user_id):
    """
    Разблокировка пользователя
    """

    user = db.session.get(User, user_id)
    if not user:
        raise NotFoundError("Пользователь не найден")

    user.status = "active"
    db.session.commit()

    return (
        jsonify(
            {
                "message": f"Пользователь {user.username} разблокирован",
                "user": user.to_dict(),
            }
        ),
        200,
    )


@admin.route("/user/<int:user_id>", methods=["PUT"])
@jwt_required()
@admin_required
def update_user(user_id):
    """
    Обновление пользователя
    """
    data = UpdateUserSchema(**request.get_json(silent=True))
    user = AdminService.update_user(user_id, data.get_updates())
    return jsonify(user.to_dict()), 200


@admin.route("/user/<int:user_id>", methods=["DELETE"])
@jwt_required()
@admin_required
def delete_user(user_id):
    """
    Удаление пользователя
    """

    user = db.session.get(User, user_id)
    if not user:
        raise NotFoundError("Пользователь не найден")

    current_user_id = int(get_jwt_identity())
    if int(user.id) == current_user_id:
        raise ValidationError("Нельзя удалить самого себя")

    db.session.delete(user)
    db.session.commit()

    return jsonify({"message": f"Пользователь {user.username} удален"}), 200


@admin.route("/motorcycles", methods=["GET"])
@jwt_required()
@admin_required
def get_motorcycles():
    """
    Получение списка всех мотоциклов для администратора
    """
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    search = request.args.get("search", "")
    filter_status = request.args.get("status", "")
    owner_id = request.args.get("owner_id", type=int)
    sort_by = request.args.get("sort_by", "created_at")
    sort_order = request.args.get("sort_order", "desc")

    query = Motorcycle.query

    # Поиск
    if search:
        query = query.filter(
            or_(
                Motorcycle.name.ilike(f"%{search}"),
                Motorcycle.vin.ilike(f"%{search}"),
                Motorcycle.license_plate.ilike(f"%{search}"),
            )
        )

    if owner_id:
        query = query.filter(Motorcycle.owner_id == owner_id)

    if filter_status:
        if filter_status == "has_maintenance":
            query = query.filter(Motorcycle.maintenances.any())
        elif filter_status == "no_maintenance":
            query = query.filter(~Motorcycle.maintenances.any())

    if sort_order == "desc":
        query = query.order_by(
            desc(getattr(Motorcycle, sort_by, Motorcycle.created_at))
        )
    else:
        query = query.order_by(getattr(Motorcycle, sort_by, Motorcycle.created_at))

    paginated = query.paginate(page=page, per_page=per_page, error_out=False)

    total_motorcycles = Motorcycle.query.count()
    with_maintenance = Motorcycle.query.filter(Motorcycle.maintenances.any()).count()
    without_maintenance = total_motorcycles - with_maintenance

    return (
        jsonify(
            {
                "motorcycles": [
                    moto.to_dict(include_owner=True, include_maintenance=True)
                    for moto in paginated.items
                ],
                "total": paginated.total,
                "pages": paginated.pages,
                "current_page": paginated.page,
                "per_page": paginated.per_page,
                "has_prev": paginated.has_prev,
                "has_next": paginated.has_next,
                "stats": {
                    "total": total_motorcycles,
                    "with_maintenance": with_maintenance,
                    "without_maintenance": without_maintenance,
                },
            }
        ),
        200,
    )


@admin.route("/motorcycle/<int:moto_id>", methods=["DELETE"])
@jwt_required()
@admin_required
def admin_delete_motorcycle(moto_id):
    """
    Удаление мотоцикла администратором
    """
    moto = db.session.get(Motorcycle, moto_id)
    if not moto:
        raise NotFoundError("Мотоцикл не найден")

    if moto.photo_url:
        from app.utils.files import delete_file

        delete_file(moto.photo_url)

    db.session.delete(moto)
    db.session.commit()

    return jsonify({"message": "Мотоцикл успешно удален"}), 200


@admin.route("/send-newsletter", methods=["POST"])
@jwt_required()
@admin_required
def send_newsletter():
    """
    Отправка рассылки только подписанным пользователям
    """
    data = request.get_json(silent=True)
    if not data:
        raise ValidationError("Нет данных")

    subject = data.get("subject")
    content = data.get("content")
    target = data.get("target", "all")

    if not subject or not content:
        raise ValidationError("Тема и содержание обязательны")

    query = User.query.filter(User.email.isnot(None))

    if target == "active":
        query = query.filter(User.status == "active")
    elif target == "admins":
        query = query.filter(User.role == "admin")

    users = query.all()
    if not users:
        raise ValidationError("Нет получателей")

    emails = [user.email for user in users if user.email]

    html_body = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; background: #f5f5f5; padding: 20px; }}
            .container {{ max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
            .header {{ text-align: center; margin-bottom: 20px; }}
            .header h1 {{ color: #7c3aed; margin: 0; }}
            .content {{ font-size: 15px; line-height: 1.6; color: #333; }}
            .footer {{ text-align: center; color: #888; font-size: 12px; margin-top: 20px; border-top: 1px solid #eee; padding-top: 20px; }}
            .unsubscribe {{ color: #7c3aed; text-decoration: none; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🏍️ MotoBind</h1>
            </div>
            <div class="content">
                {content}
            </div>
        </div>
    </body>
    </html>
    """

    app = current_app._get_current_object()
    result = EmailService.send_bulk_email(app, emails, subject, html_body)

    return (
        jsonify(
            {
                "message": "Рассылка запущена",
                "total": len(emails),
                "target": target,
                "result": result,
            }
        ),
        200,
    )


@admin.route("/reports", methods=["GET"])
@jwt_required()
@admin_required
def get_reports():
    """Список жалоб на посты"""
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 20, type=int)
    status = request.args.get("status") or None
    category = request.args.get("category") or None

    data = ReportService.get_reports(
        page=page, per_page=per_page, status=status, category=category
    )
    return jsonify(data), 200


@admin.route("/reports/<int:report_id>", methods=["GET"])
@jwt_required()
@admin_required
def get_report(report_id):
    report = db.session.get(PostReport, report_id)
    if not report:
        raise NotFoundError("Жалоба не найдена")
    return jsonify(report.to_dict()), 200


@admin.route("/reports/<int:report_id>/resolve", methods=["POST"])
@jwt_required()
@admin_required
def resolve_report(report_id):
    """
    Рассмотреть жалобу.
    body: { action: 'post_deleted' | 'user_banned' | 'both' | 'none', note?: str }
    """
    data = request.get_json(silent=True) or {}
    action = data.get("action")
    note = data.get("note")
    admin_id = int(get_jwt_identity())

    if action == "none":
        report = ReportService.reject_report(report_id, admin_id, note)
    else:
        report = ReportService.resolve_report(report_id, admin_id, action, note)

    return (
        jsonify(
            {
                "message": "Жалоба рассмотрена",
                "report": report.to_dict(),
            }
        ),
        200,
    )


@admin.route("/reports/<int:report_id>", methods=["DELETE"])
@jwt_required()
@admin_required
def delete_report(report_id):
    report = db.session.get(PostReport, report_id)
    if not report:
        raise NotFoundError("Жалоба не найдена")
    db.session.delete(report)
    db.session.commit()
    return jsonify({"message": "Жалоба удалена"}), 200


@admin.route("/cron/run-reminders", methods=["POST"])
def cron_run_reminders():
    """
    Ручной запуск cron-задачи напоминаний.

    Защищён секретным ключом (не JWT), чтобы внешний cron мог дёргать.
    Ключ передаётся в заголовке X-Cron-Secret.

    Использование (Linux crontab):
        0 9 * * * curl -X POST https://motobind.ru/api/admin/cron/run-reminders \
                           -H "X-Cron-Secret: ВАШ_СЕКРЕТ"

    Использование (Windows Task Scheduler):
        curl.exe -X POST https://motobind.ru/api/admin/cron/run-reminders ^
                 -H "X-Cron-Secret: ВАШ_СЕКРЕТ"
    """
    import os

    from flask import current_app

    secret = current_app.config.get("CRON_SECRET")
    if not secret:
        current_app.logger.error("[Cron] CRON_SECRET не настроен")
        return jsonify({"error": "Cron endpoint не настроен"}), 503

    provided = request.headers.get("X-Cron-Secret")
    if not provided or provided != secret:
        current_app.logger.warning("[Cron] Неверный CRON_SECRET")
        return jsonify({"error": "Forbidden"}), 403

    try:
        stats = ReminderService.run_daily_check()
        current_app.logger.info(f"[Cron] run_daily_check: {stats}")
        return (
            jsonify(
                {
                    "message": "Cron задача выполнена",
                    "stats": stats,
                }
            ),
            200,
        )
    except Exception as e:
        current_app.logger.exception("[Cron] run_daily_check failed")
        return (
            jsonify(
                {
                    "error": "Внутренняя ошибка",
                    "detail": str(e),
                }
            ),
            500,
        )


@admin.route("/services", methods=["GET"])
@jwt_required()
@admin_required
def admin_list_services():
    """Список услуг для модерации."""
    status = request.args.get("status") or None
    search = request.args.get("search", "")

    items = ServiceService.list_for_admin(status=status, search=search)
    return jsonify([s.to_dict() for s in items]), 200


@admin.route("/services/<int:service_id>/approve", methods=["POST"])
@jwt_required()
@admin_required
def admin_approve_service(service_id):
    service = ServiceService.approve(service_id)
    return (
        jsonify(
            {
                "message": "Услуга одобрена",
                "service": service.to_dict(),
            }
        ),
        200,
    )
