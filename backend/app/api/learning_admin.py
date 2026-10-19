"""
Админские роуты раздела «Обучение».

Все требуют JWT + роль 'admin'.

Курсы:
    GET    /api/learning/admin/courses
    GET    /api/learning/admin/courses/<id>
    POST   /api/learning/admin/courses
    PUT    /api/learning/admin/courses/<id>
    DELETE /api/learning/admin/courses/<id>
    POST   /api/learning/admin/courses/<id>/publish
    POST   /api/learning/admin/courses/<id>/archive

Уроки:
    GET    /api/learning/admin/lessons/<id>
    POST   /api/learning/admin/courses/<id>/lessons
    PUT    /api/learning/admin/lessons/<id>
    DELETE /api/learning/admin/lessons/<id>
    POST   /api/learning/admin/courses/<id>/lessons/reorder

Статьи:
    GET    /api/learning/admin/articles
    GET    /api/learning/admin/articles/<id>
    POST   /api/learning/admin/articles
    PUT    /api/learning/admin/articles/<id>
    DELETE /api/learning/admin/articles/<id>
    POST   /api/learning/admin/articles/<id>/publish
    POST   /api/learning/admin/articles/<id>/archive

Загрузка обложек:
    POST   /api/learning/admin/upload/cover
"""

import os
import uuid

from app.decorators import admin_required
from app.exceptions import NotFoundError, ValidationError
from app.schemas.article import ArticleCreateSchema, ArticleUpdateSchema
from app.schemas.course import CourseCreateSchema, CourseUpdateSchema
from app.schemas.lesson import (
    LessonCreateSchema,
    LessonReorderSchema,
    LessonUpdateSchema,
)
from app.services.learning_service import LearningService
from app.utils.helpers import get_current_user_id
from flask import Blueprint, current_app, jsonify, request
from werkzeug.utils import secure_filename

learning_admin = Blueprint("learning_admin", __name__)


# ============================================================
# КУРСЫ
# ============================================================


@learning_admin.route("/courses", methods=["GET"])
@admin_required
def admin_list_courses():
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 20, type=int)
    data = LearningService.admin_list_courses(page=page, per_page=per_page)
    return jsonify(data), 200


@learning_admin.route("/courses/<int:course_id>", methods=["GET"])
@admin_required
def admin_get_course(course_id):
    data = LearningService.admin_get_course(course_id)
    return jsonify(data), 200


@learning_admin.route("/courses", methods=["POST"])
@admin_required
def admin_create_course():
    schema = CourseCreateSchema.model_validate(request.get_json() or {})
    course = LearningService.create_course(
        author_id=get_current_user_id(),
        data=schema.model_dump(),
    )
    data = LearningService.admin_get_course(course.id)
    return jsonify(data), 201


@learning_admin.route("/courses/<int:course_id>", methods=["PUT"])
@admin_required
def admin_update_course(course_id):
    schema = CourseUpdateSchema.model_validate(request.get_json() or {})
    LearningService.update_course(course_id, schema.get_updates())
    data = LearningService.admin_get_course(course_id)
    return jsonify(data), 200


@learning_admin.route("/courses/<int:course_id>", methods=["DELETE"])
@admin_required
def admin_delete_course(course_id):
    LearningService.delete_course(course_id)
    return jsonify({"message": "Курс удалён"}), 200


@learning_admin.route("/courses/<int:course_id>/publish", methods=["POST"])
@admin_required
def admin_publish_course(course_id):
    LearningService.publish_course(course_id)
    data = LearningService.admin_get_course(course_id)
    return jsonify(data), 200


@learning_admin.route("/courses/<int:course_id>/archive", methods=["POST"])
@admin_required
def admin_archive_course(course_id):
    LearningService.archive_course(course_id)
    data = LearningService.admin_get_course(course_id)
    return jsonify(data), 200


# ============================================================
# УРОКИ
# ============================================================


@learning_admin.route("/lessons/<int:lesson_id>", methods=["GET"])
@admin_required
def admin_get_lesson(lesson_id):
    data = LearningService.admin_get_lesson(lesson_id)
    return jsonify(data), 200


@learning_admin.route("/courses/<int:course_id>/lessons", methods=["POST"])
@admin_required
def admin_create_lesson(course_id):
    schema = LessonCreateSchema.model_validate(request.get_json() or {})
    lesson = LearningService.create_lesson(course_id, schema.model_dump())
    return (
        jsonify(
            {
                "id": lesson.id,
                "slug": lesson.slug,
                "order": lesson.order,
                "title": lesson.title,
            }
        ),
        201,
    )


@learning_admin.route("/lessons/<int:lesson_id>", methods=["PUT"])
@admin_required
def admin_update_lesson(lesson_id):
    schema = LessonUpdateSchema.model_validate(request.get_json() or {})
    lesson = LearningService.update_lesson(lesson_id, schema.get_updates())
    return (
        jsonify(
            {
                "id": lesson.id,
                "slug": lesson.slug,
                "order": lesson.order,
                "title": lesson.title,
            }
        ),
        200,
    )


@learning_admin.route("/lessons/<int:lesson_id>", methods=["DELETE"])
@admin_required
def admin_delete_lesson(lesson_id):
    LearningService.delete_lesson(lesson_id)
    return jsonify({"message": "Урок удалён"}), 200


@learning_admin.route("/courses/<int:course_id>/lessons/reorder", methods=["POST"])
@admin_required
def admin_reorder_lessons(course_id):
    schema = LessonReorderSchema.model_validate(request.get_json() or {})
    LearningService.reorder_lessons(course_id, [i.model_dump() for i in schema.items])
    data = LearningService.admin_get_course(course_id)
    return jsonify(data), 200


# ============================================================
# СТАТЬИ
# ============================================================


@learning_admin.route("/articles", methods=["GET"])
@admin_required
def admin_list_articles():
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 20, type=int)
    data = LearningService.admin_list_articles(page=page, per_page=per_page)
    return jsonify(data), 200


@learning_admin.route("/articles/<int:article_id>", methods=["GET"])
@admin_required
def admin_get_article(article_id):
    data = LearningService.admin_get_article(article_id)
    return jsonify(data), 200


@learning_admin.route("/articles", methods=["POST"])
@admin_required
def admin_create_article():
    schema = ArticleCreateSchema.model_validate(request.get_json() or {})
    article = LearningService.create_article(
        author_id=get_current_user_id(),
        data=schema.model_dump(),
    )
    data = LearningService.admin_get_article(article.id)
    return jsonify(data), 201


@learning_admin.route("/articles/<int:article_id>", methods=["PUT"])
@admin_required
def admin_update_article(article_id):
    schema = ArticleUpdateSchema.model_validate(request.get_json() or {})
    LearningService.update_article(article_id, schema.get_updates())
    data = LearningService.admin_get_article(article_id)
    return jsonify(data), 200


@learning_admin.route("/articles/<int:article_id>", methods=["DELETE"])
@admin_required
def admin_delete_article(article_id):
    LearningService.delete_article(article_id)
    return jsonify({"message": "Статья удалена"}), 200


@learning_admin.route("/articles/<int:article_id>/publish", methods=["POST"])
@admin_required
def admin_publish_article(article_id):
    LearningService.publish_article(article_id)
    data = LearningService.admin_get_article(article_id)
    return jsonify(data), 200


@learning_admin.route("/articles/<int:article_id>/archive", methods=["POST"])
@admin_required
def admin_archive_article(article_id):
    LearningService.archive_article(article_id)
    data = LearningService.admin_get_article(article_id)
    return jsonify(data), 200


# ============================================================
# ЗАГРУЗКА ОБЛОЖЕК
# ============================================================

ALLOWED_IMAGE_EXTENSIONS = {"jpg", "jpeg", "png", "webp", "gif"}


@learning_admin.route("/upload/cover", methods=["POST"])
@admin_required
def admin_upload_cover():
    """
    Загрузка обложки курса/урока/статьи.
    Multipart: поле 'file'.
    Возвращает: { "url": "learning/covers/<filename>" }
    """
    if "file" not in request.files:
        raise ValidationError("Файл не найден")

    file = request.files["file"]
    if not file or file.filename == "":
        raise ValidationError("Файл не выбран")

    filename_lower = file.filename.lower()
    ext = filename_lower.rsplit(".", 1)[-1] if "." in filename_lower else ""
    if ext not in ALLOWED_IMAGE_EXTENSIONS:
        raise ValidationError(
            f"Недопустимый формат. Разрешены: {', '.join(ALLOWED_IMAGE_EXTENSIONS)}"
        )

    unique_name = f"{uuid.uuid4().hex}.{ext}"
    safe_name = secure_filename(unique_name)

    upload_dir = os.path.join(current_app.config["UPLOAD_FOLDER"], "learning", "covers")
    os.makedirs(upload_dir, exist_ok=True)

    filepath = os.path.join(upload_dir, safe_name)
    file.save(filepath)

    return jsonify({"url": f"learning/covers/{safe_name}"}), 200
