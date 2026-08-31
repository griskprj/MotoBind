from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from sqlalchemy import desc, or_

from app.decorators import admin_required
from app.exceptions import NotFoundError, ValidationError
from app.extensions import db
from app.models.manual import Manual
from app.models.motorcycle import Motorcycle
from app.models.user import User
from app.schemas.admin import CreateUserSchema, UpdateUserSchema
from app.services.admin_service import AdminService
from app.services.notification_service import NotificationService

admin = Blueprint("admin", __name__)


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
    manual = Manual.query.get(manual_id)
    if not manual:
        raise NotFoundError("Мануал не найден")

    if manual.status != "moderate":
        raise ValidationError(f"Мануал уже обработан (статус: {manual.status})")

    manual.status = "approved"
    db.session.commit()

    NotificationService.send_notification(
        user_id=manual.author_id,
        type='manual_status',
        title='Мануал одобрен',
        content=f'Ваш мануал "{manual.title}" был одобрен и опубликован.',
        link=f'/manual/{manual.id}',
        extra_data={'manual_id': manual.id, 'status': 'approved'}
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

    manual = Manual.query.get(manual_id)
    if not manual:
        raise NotFoundError("Мануал не найден")

    if manual.status != "moderate":
        raise ValidationError(f"Мануал уже обработан (статус: {manual.status})")

    data = request.get_json()
    if not data:
        raise ValidationError("Нет данных")

    reason = data.get("reason", "Без указания причины")

    manual.status = "rejected"
    manual.rejection_reason = reason

    db.session.commit()

    NotificationService.send_notification(
        user_id=manual.author_id,
        type='manual_status',
        title='Мануал отклонен',
        content=f'Ваш мануал "{manual.title}" был отклонен. Причина: {reason}',
        link=f'/manual/{manual.id}',
        extra_data={'manual_id': manual.id, 'status': 'rejected', 'reason': reason}
    )

    return jsonify({"message": "Мануал отклонен", "manual": manual.to_dict()}), 200


@admin.route("/manual/<int:manual_id>/reconsider", methods=["POST"])
@jwt_required()
@admin_required
def reconsider_manual(manual_id):
    """
    Пересмотр мануала
    """

    manual = Manual.query.get(manual_id)
    if not manual:
        raise NotFoundError("Мануал не найден")

    if manual.status == "moderate":
        raise ValidationError("Мануал уже на проверке")

    manual.status = "moderate"
    manual.rejection_reason = None
    db.session.commit()

    NotificationService.send_notification(
        user_id=manual.author_id,
        type='manual_status',
        title='Мануал отправлен на повторную проверку',
        content=f'Ваш мануал "{manual.title}" отправлен на повторную проверку.',
        link=f'/manual/{manual.id}',
        extra_data={'manual_id': manual.id, 'status': 'moderate'}
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

    manual = Manual.query.get(manual_id)
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
    data = CreateUserSchema(**request.get_json())
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

    user = User.query.get(user_id)
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

    user = User.query.get(user_id)
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
    data = UpdateUserSchema(**request.get_json())
    user = AdminService.update_user(user_id, data.get_updates())
    return jsonify(user.to_dict()), 200


@admin.route("/user/<int:user_id>", methods=["DELETE"])
@jwt_required()
@admin_required
def delete_user(user_id):
    """
    Удаление пользователя
    """

    user = User.query.get(user_id)
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
        query = query.order_by(desc(getattr(Motorcycle, sort_by, Motorcycle.created_at)))
    else:
        query = query.order_by(getattr(Motorcycle, sort_by, Motorcycle.created_at))

    paginated = query.paginate(page=page, per_page=per_page, error_out=False)

    total_motorcycles = Motorcycle.query.count()
    with_maintenance = Motorcycle.query.filter(Motorcycle.maintenances.any()).count()
    without_maintenance = total_motorcycles - with_maintenance

    return jsonify(
        {
            "motorcycles": [
                moto.to_dict(
                    include_owner=True,
                    include_maintenance=True
                ) for moto in paginated.items
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
            }
        }
    ), 200


@admin.route("/motorcycle/<int:moto_id>", methods=["DELETE"])
@jwt_required()
@admin_required
def admin_delete_motorcycle(moto_id):
    """
    Удаление мотоцикла администратором
    """
    moto = Motorcycle.query.get(moto_id)
    if not moto:
        raise NotFoundError("Мотоцикл не найден")

    # Удаляем фото
    if moto.photo_url:
        from app.utils.files import delete_file
        delete_file(moto.photo_url)

    db.session.delete(moto)
    db.session.commit()

    return jsonify({"message": "Мотоцикл успешно удален"}), 200