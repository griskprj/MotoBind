"""
Роуты раздела «Обучение» — публичные и приватные (JWT).

Публичные:
    GET /api/learning/courses
    GET /api/learning/courses/<slug>
    GET /api/learning/courses/<slug>/lessons/<lesson_slug>
    GET /api/learning/articles
    GET /api/learning/articles/<slug>

Приватные (JWT):
    POST   /api/learning/courses/<slug>/lessons/<lesson_slug>/complete
    DELETE /api/learning/courses/<slug>/lessons/<lesson_slug>/complete
    GET    /api/learning/my
"""

from app.schemas.article import ArticleDetailSchema, ArticleListResponseSchema
from app.schemas.course import CourseDetailSchema, CourseListResponseSchema
from app.schemas.learning_my import MyLearningResponseSchema
from app.schemas.learning_progress import CompleteLessonResponseSchema
from app.schemas.lesson import LessonDetailSchema
from app.services.learning_service import LearningService
from app.utils.helpers import get_current_user_id
from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required, verify_jwt_in_request
from flask_jwt_extended.exceptions import NoAuthorizationError

learning = Blueprint("learning", __name__)


# ============================================================
# ХЕЛПЕРЫ
# ============================================================


def _optional_user_id():
    """
    Возвращает user_id, если передан валидный JWT, иначе None.
    Не бросает исключений — используется на публичных роутах.
    """
    try:
        verify_jwt_in_request(optional=True)
        identity = get_jwt_identity()
        return int(identity) if identity else None
    except NoAuthorizationError:
        return None
    except Exception:
        return None


def _parse_bool(value):
    """'true' / '1' / 'yes' → True, 'false' / '0' / 'no' → False, иначе None."""
    if value is None:
        return None
    v = str(value).strip().lower()
    if v in ("true", "1", "yes"):
        return True
    if v in ("false", "0", "no"):
        return False
    return None


# ============================================================
# КУРСЫ — ПУБЛИЧНЫЕ
# ============================================================


@learning.route("/courses", methods=["GET"])
def list_courses():
    """Публичный список опубликованных курсов."""
    user_id = _optional_user_id()

    data = LearningService.list_courses(
        user_id=user_id,
        category=request.args.get("category") or None,
        level=request.args.get("level") or None,
        is_free=_parse_bool(request.args.get("is_free")),
        search=request.args.get("search", ""),
        page=request.args.get("page", 1, type=int),
        per_page=request.args.get("per_page", 12, type=int),
    )
    payload = CourseListResponseSchema.model_validate(data).model_dump()
    return jsonify(payload), 200


@learning.route("/courses/<string:course_slug>", methods=["GET"])
def get_course(course_slug):
    """Публичная страница курса с программой."""
    user_id = _optional_user_id()

    data = LearningService.get_course_detail(user_id=user_id, course_slug=course_slug)
    payload = CourseDetailSchema.model_validate(data).model_dump()
    return jsonify(payload), 200


@learning.route(
    "/courses/<string:course_slug>/lessons/<string:lesson_slug>",
    methods=["GET"],
)
def get_lesson(course_slug, lesson_slug):
    """
    Контент урока.

    Гость: доступ к бесплатным курсам и превью-урокам.
    Авторизованный: то же + upsert UserCourseState.
    Закрытый урок → 403.
    """
    user_id = _optional_user_id()

    data = LearningService.get_lesson_detail(
        user_id=user_id,
        course_slug=course_slug,
        lesson_slug=lesson_slug,
    )
    payload = LessonDetailSchema.model_validate(data).model_dump()
    return jsonify(payload), 200


# ============================================================
# СТАТЬИ — ПУБЛИЧНЫЕ
# ============================================================


@learning.route("/articles", methods=["GET"])
def list_articles():
    """Публичный список опубликованных статей."""
    data = LearningService.list_articles(
        category=request.args.get("category") or None,
        tag=request.args.get("tag") or None,
        search=request.args.get("search", ""),
        page=request.args.get("page", 1, type=int),
        per_page=request.args.get("per_page", 12, type=int),
    )
    payload = ArticleListResponseSchema.model_validate(data).model_dump()
    return jsonify(payload), 200


@learning.route("/articles/<string:article_slug>", methods=["GET"])
def get_article(article_slug):
    """Публичная страница статьи + похожие."""
    data = LearningService.get_article_detail(article_slug=article_slug)
    payload = ArticleDetailSchema.model_validate(data).model_dump()
    return jsonify(payload), 200


# ============================================================
# ПРОГРЕСС — ПРИВАТНЫЕ
# ============================================================


@learning.route(
    "/courses/<string:course_slug>/lessons/<string:lesson_slug>/complete",
    methods=["POST"],
)
@jwt_required()
def complete_lesson(course_slug, lesson_slug):
    """Отметить урок пройденным."""
    user_id = get_current_user_id()
    data = LearningService.complete_lesson(
        user_id=user_id,
        course_slug=course_slug,
        lesson_slug=lesson_slug,
    )
    payload = CompleteLessonResponseSchema.model_validate(data).model_dump()
    return jsonify(payload), 200


@learning.route(
    "/courses/<string:course_slug>/lessons/<string:lesson_slug>/complete",
    methods=["DELETE"],
)
@jwt_required()
def uncomplete_lesson(course_slug, lesson_slug):
    """Отменить отметку «пройдено»."""
    user_id = get_current_user_id()
    data = LearningService.uncomplete_lesson(
        user_id=user_id,
        course_slug=course_slug,
        lesson_slug=lesson_slug,
    )
    payload = CompleteLessonResponseSchema.model_validate(data).model_dump()
    return jsonify(payload), 200


@learning.route("/my", methods=["GET"])
@jwt_required()
def my_learning():
    """Моё обучение — три группы курсов."""
    user_id = get_current_user_id()
    data = LearningService.get_my_learning(user_id=user_id)
    payload = MyLearningResponseSchema.model_validate(data).model_dump()
    return jsonify(payload), 200
