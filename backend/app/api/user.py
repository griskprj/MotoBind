from flask import Blueprint, current_app, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer

from app.exceptions import ForbiddenError, NotFoundError, ValidationError
from app.extensions import db
from app.schemas.user import ChangePasswordSchema, UpdateProfileSchema
from app.services.post_service import PostService
from app.services.user_service import UserService

user = Blueprint("user", __name__)


@user.route("/profile", methods=["PUT"])
@jwt_required()
def update_profile():
    """Обновление профиля"""
    try:
        user_id = int(get_jwt_identity())
        data = request.get_json()
        schema = UpdateProfileSchema(**data)
        updates = schema.get_updates()

        user_obj = UserService.update_profile(user_id, **updates)
        return jsonify(user_obj.to_dict()), 200
    except ValidationError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@user.route("/profile/<int:user_id>", methods=["GET"])
@jwt_required()
def get_public_profile(user_id):
    """Получение публичного профиля пользователя"""
    try:
        current_user_id = int(get_jwt_identity())
        user_obj = UserService.get_user_by_id(user_id)

        posts_data = PostService.get_posts(
            page=1, per_page=5, user_id=user_id, current_user_id=current_user_id, include_comments=False
        )

        return jsonify({"user": user_obj.to_dict(include_stats=True), "recent_posts": posts_data["posts"]}), 200
    except NotFoundError as e:
        return jsonify({"error": str(e)}), 404


@user.route("/profile/me", methods=["GET"])
@jwt_required()
def get_my_profile():
    """Получение своего профиля (полная информация)"""
    user_id = int(get_jwt_identity())
    user_obj = UserService.get_user_by_id(user_id)
    return (
        jsonify(
            {
                "user": user_obj.to_dict(include_moto=True, include_stats=True),
            }
        ),
        200,
    )


@user.route("/notification-settings", methods=["GET"])
@jwt_required()
def get_notification_settings():
    user = UserService.get_user_by_id(int(get_jwt_identity()))

    return (
        jsonify(
            {
                "email_notifications_enabled": user.email_notifications_enabled,
                "email_newsletter_enabled": user.email_newsletter_enabled,
                "email_verification_enabled": user.email_verification_enabled,
                "reminders_mileage_enabled": user.reminders_mileage_enabled,
                "reminders_maintenance_enabled": user.reminders_maintenance_enabled,
            }
        ),
        200,
    )


@user.route("/notification-settings", methods=["PUT"])
@jwt_required()
def update_notification_settings():
    user = UserService.get_user_by_id(int(get_jwt_identity()))
    data = request.get_json() or {}

    bool_fields = (
        "email_notifications_enabled",
        "email_newsletter_enabled",
        "email_verification_enabled",
        "reminders_mileage_enabled",
        "reminders_maintenance_enabled",
    )

    for field in bool_fields:
        if field in data:
            setattr(user, field, bool(data[field]))

    db.session.commit()

    return (
        jsonify(
            {
                "message": "Настройки уведомлений обновлены",
                "settings": {
                    "email_notifications_enabled": user.email_notifications_enabled,
                    "email_newsletter_enabled": user.email_newsletter_enabled,
                    "email_verification_enabled": user.email_verification_enabled,
                    "reminders_mileage_enabled": user.reminders_mileage_enabled,
                    "reminders_maintenance_enabled": user.reminders_maintenance_enabled,
                },
            }
        ),
        200,
    )


@user.route("/unsubscribe/<string:token>", methods=["GET"])
def unsubscribe_from_newsletter(token):
    """Отписка от рассылки по токену"""
    try:
        serializer = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
        email = serializer.loads(token, max_age=31536000)
    except (BadSignature, SignatureExpired):
        return jsonify({"error": "Недействительная ссылка"}), 400

    user = UserService.get_user_by_email(email=email)
    user.email_newsletter_enabled = False
    db.session.commit()

    return jsonify({"message": "Вы успешно отписались от рассылки", "email": email}), 200


@user.route("/unsubscribe/<string:token>", methods=["POST"])
def unscubcsribe_direct(email):
    """Отписка от рассылки по email (без токена, для админов)"""
    user = UserService.get_user_by_email(email=email)
    user.email_newsletter_enabled = False
    db.session.commit()

    return jsonify({"message": f"Пользователь {email} отписан от рассылки"}), 200


@user.route("/avatar", methods=["POST"])
@jwt_required()
def upload_avatar():
    """
    Загрузить аватар
    """
    if "avatar" not in request.files:
        return jsonify({"error": "Файл не найден"}), 400

    file = request.files["avatar"]
    if file.filename == "":
        return jsonify({"error": "Файл не выбран"}), 400

    user_id = int(get_jwt_identity())
    user = UserService.update_avatar(user_id, file)

    return jsonify(user.to_dict()), 200


@user.route("/avatar", methods=["DELETE"])
@jwt_required()
def delete_avatar():
    """
    Удалить аватар
    """
    user_id = int(get_jwt_identity())
    user = UserService.delete_avatar(user_id)

    return jsonify(user.to_dict()), 200


@user.route("/change-password", methods=["PATCH"])
@jwt_required()
def change_password():
    """
    Изменить пароль
    """

    data = ChangePasswordSchema(**request.get_json())
    user = UserService.change_password(
        user_id=int(get_jwt_identity()),
        current_password=data.currentPassword,
        new_password=data.newPassword,
    )
    return jsonify(user.to_dict()), 200


@user.route("/account", methods=["DELETE"])
@jwt_required()
def delete_account():
    """
    Удалить аккаунт
    """

    current_user_id = int(get_jwt_identity())
    user = UserService.get_user_by_id(current_user_id)
    data = request.get_json()

    if not (user.check_password(data.get("password"))):
        raise ForbiddenError("Неверный пароль")

    if user.avatar:
        from app.utils.files import delete_file

        delete_file(user.avatar)

    db.session.delete(user)
    db.session.commit()

    return jsonify({"message": "Аккаунт удален. Возвращайтесь)"}), 200
