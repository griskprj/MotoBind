"""
Social API — тонкие контроллеры.

Вся бизнес-логика — в services/post_service.py и services/report_service.py.
"""
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from app.models.post_report import PostReport
from app.schemas.social import (
    CommentResponseSchema,
    LikeToggleResponseSchema,
    PostDetailResponseSchema,
    PostListResponseSchema,
    PostResponseSchema,
    ReportCategorySchema,
    ReportResponseSchema,
)
from app.services.post_service import PostService
from app.services.report_service import ReportService
from app.utils.helpers import get_current_user_id

social_bp = Blueprint("social", __name__)


# ---- Posts ----

@social_bp.route("/posts", methods=["POST"])
@jwt_required()
def create_post():
    """Создание поста."""
    user_id = get_current_user_id()
    content = request.form.get("content")
    image = request.files.get("image")

    result = PostService.create_post(user_id, content, image)
    return jsonify(PostResponseSchema.model_validate(result).model_dump()), 201


@social_bp.route("/posts", methods=["GET"])
@jwt_required()
def get_posts():
    """Лента постов."""
    current_user_id = get_current_user_id()
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 20, type=int)
    user_id = request.args.get("user_id", type=int)
    include_comments = request.args.get("include_comments", "false").lower() == "true"

    data = PostService.get_posts(
        page=page,
        per_page=per_page,
        user_id=user_id,
        current_user_id=current_user_id,
        include_comments=include_comments,
    )
    return jsonify(PostListResponseSchema.model_validate(data).model_dump()), 200


@social_bp.route("/posts/<int:post_id>", methods=["GET"])
@jwt_required()
def get_post(post_id):
    """Один пост."""
    current_user_id = get_current_user_id()
    include_comments = request.args.get("include_comments", "true").lower() == "true"

    post_data = PostService.get_post(
        post_id=post_id,
        current_user_id=current_user_id,
        include_comments=include_comments,
    )
    return jsonify(PostResponseSchema.model_validate(post_data).model_dump()), 200


@social_bp.route("/posts/<int:post_id>", methods=["PUT"])
@jwt_required()
def update_post(post_id):
    """Обновление поста."""
    user_id = get_current_user_id()
    content = request.form.get("content")
    image = request.files.get("image")

    result = PostService.update_post(post_id, user_id, content, image)
    return jsonify(PostResponseSchema.model_validate(result).model_dump()), 200


@social_bp.route("/posts/<int:post_id>", methods=["DELETE"])
@jwt_required()
def delete_post(post_id):
    """Удаление поста."""
    user_id = get_current_user_id()
    PostService.delete_post(post_id, user_id)
    return jsonify({"message": "Пост удалён"}), 200


# ---- Likes ----

@social_bp.route("/posts/<int:post_id>/like", methods=["POST"])
@jwt_required()
def toggle_like(post_id):
    """Поставить/убрать лайк."""
    user_id = get_current_user_id()
    result = PostService.toggle_like(post_id, user_id)
    return jsonify(LikeToggleResponseSchema.model_validate(result).model_dump()), 200


# ---- Comments ----

@social_bp.route("/posts/<int:post_id>/comments", methods=["POST"])
@jwt_required()
def add_comment(post_id):
    """Добавить комментарий."""
    user_id = get_current_user_id()
    data = request.get_json() or {}

    comment = PostService.add_comment(post_id, user_id, data.get("content"))
    return jsonify(CommentResponseSchema.model_validate(comment.to_dict()).model_dump()), 201


@social_bp.route("/comments/<int:comment_id>", methods=["DELETE"])
@jwt_required()
def delete_comment(comment_id):
    """Удалить комментарий."""
    user_id = get_current_user_id()
    PostService.delete_comment(comment_id, user_id)
    return jsonify({"message": "Комментарий удалён"}), 200


# ---- Reports ----

@social_bp.route("/posts/<int:post_id>/report", methods=["POST"])
@jwt_required()
def report_post(post_id):
    """Отправить жалобу на пост."""
    user_id = get_current_user_id()
    data = request.get_json() or {}

    report = ReportService.create_report(
        post_id=post_id,
        reporter_id=user_id,
        category=data.get("category"),
        description=data.get("description"),
    )
    report_dict = report.to_dict(include_post=False)
    return jsonify({
        "message": "Жалоба отправлена модератору",
        "report": ReportResponseSchema.model_validate(report_dict).model_dump(),
    }), 201


@social_bp.route("/report-categories", methods=["GET"])
@jwt_required()
def get_report_categories():
    """Список категорий жалоб."""
    return jsonify([
        ReportCategorySchema.model_validate({"value": k, "label": v}).model_dump()
        for k, v in PostReport.CATEGORIES.items()
    ]), 200