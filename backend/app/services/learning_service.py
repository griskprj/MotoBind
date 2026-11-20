"""
Сервис для работы с разделом «Обучение»:
курсы, уроки, статьи, прогресс.
"""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from app.exceptions import ForbiddenError, NotFoundError, ValidationError
from app.extensions import db
from app.models.article import Article
from app.models.course import Course
from app.models.learning_enums import ContentStatus
from app.models.lesson import Lesson
from app.models.user_course_progress import UserCourseProgress
from app.models.user_course_state import UserCourseState
from sqlalchemy import func, or_
from sqlalchemy.orm import joinedload, selectinload


class LearningService:
    """Сервис раздела «Обучение»."""

    # ============================================================
    # ДОСТУП
    # ============================================================

    @staticmethod
    def can_access_course(user_id: Optional[int], course: Course) -> bool:
        """
        Может ли пользователь видеть курс целиком.
        Публичные курсы — да. Платные — только при наличии покупки.
        На MVP-1 покупок нет, поэтому платные курсы доступны только для просмотра
        описания, но не контента.
        """
        if course.is_free:
            return True
        if user_id is None:
            return False
        return False

    @staticmethod
    def can_access_lesson(user_id: Optional[int], lesson: Lesson) -> bool:
        """Может ли пользователь открыть контент урока."""
        course = lesson.course
        if course is None:
            return False
        if course.is_free:
            return True
        if lesson.is_free_preview:
            return True
        if user_id is None:
            return False
        # MVP-1: покупок нет
        return False

    # ============================================================
    # ХЕЛПЕРЫ
    # ============================================================

    @staticmethod
    def _paginate(query, page: int, per_page: int) -> Dict[str, Any]:
        """Пагинация с метаданными в формате PaginationSchema."""
        page = max(1, page)
        per_page = max(1, min(per_page, 100))

        total = query.count()
        pages = (total + per_page - 1) // per_page if total > 0 else 0
        items = query.offset((page - 1) * per_page).limit(per_page).all()

        return {
            "items": items,
            "pagination": {
                "total": total,
                "page": page,
                "per_page": per_page,
                "pages": pages,
                "has_prev": page > 1,
                "has_next": page < pages,
            },
        }

    @staticmethod
    def _author_dict(user) -> Optional[dict]:
        if user is None:
            return None
        return {"id": user.id, "username": user.username}

    @staticmethod
    def _course_to_short(course: Course, *, is_purchased: bool = False) -> dict:
        """Сериализация курса для списка."""
        return {
            "id": course.id,
            "slug": course.slug,
            "title": course.title,
            "short_description": course.short_description,
            "cover_url": course.cover_url,
            "category": course.category.value if course.category else None,
            "level": course.level.value if course.level else None,
            "price": course.price,
            "is_free": course.is_free,
            "lessons_count": course.lessons_count,
            "author": LearningService._author_dict(course.author),
            "created_at": course.created_at.isoformat() if course.created_at else None,
            "published_at": (
                course.published_at.isoformat() if course.published_at else None
            ),
            "is_purchased": is_purchased,
        }

    @staticmethod
    def _course_to_detail(
        course: Course,
        *,
        user_id: Optional[int],
        completed_lesson_ids: set,
        is_purchased: bool,
        last_viewed_lesson_id: Optional[int],
    ) -> dict:
        """Сериализация курса для страницы курса."""
        lessons = []
        for lesson in course.lessons:
            accessible = LearningService.can_access_lesson(user_id, lesson)
            lessons.append(
                {
                    "id": lesson.id,
                    "slug": lesson.slug,
                    "order": lesson.order,
                    "title": lesson.title,
                    "is_free_preview": lesson.is_free_preview,
                    "has_video": bool(lesson.video_url),
                    "video_duration": lesson.video_duration,
                    "is_completed": lesson.id in completed_lesson_ids,
                    "is_accessible": accessible,
                }
            )

        total = len(course.lessons)
        completed = sum(1 for l in course.lessons if l.id in completed_lesson_ids)

        data = LearningService._course_to_short(course, is_purchased=is_purchased)
        data.update(
            {
                "description": course.description,
                "lessons": lessons,
                "progress": {"completed": completed, "total": total},
                "last_viewed_lesson_id": last_viewed_lesson_id,
            }
        )
        return data

    @staticmethod
    def _article_to_short(article: Article) -> dict:
        return {
            "id": article.id,
            "slug": article.slug,
            "title": article.title,
            "short_description": article.short_description,
            "cover_url": article.cover_url,
            "category": article.category.value if article.category else None,
            "tags": article.tags or [],
            "author": LearningService._author_dict(article.author),
            "created_at": article.created_at.isoformat()
            if article.created_at
            else None,
            "published_at": (
                article.published_at.isoformat() if article.published_at else None
            ),
        }

    @staticmethod
    def _article_to_detail(article: Article, related: List[Article]) -> dict:
        data = LearningService._article_to_short(article)
        data.update(
            {
                "content": article.content,
                "updated_at": (
                    article.updated_at.isoformat() if article.updated_at else None
                ),
                "related": [LearningService._article_to_short(a) for a in related],
            }
        )
        return data

    @staticmethod
    def _get_completed_lesson_ids(user_id: Optional[int], course_id: int) -> set:
        """Множество id пройденных уроков пользователя в курсе."""
        if user_id is None:
            return set()
        rows = (
            db.session.query(UserCourseProgress.lesson_id)
            .filter_by(user_id=user_id, course_id=course_id)
            .all()
        )
        return {r[0] for r in rows}

    @staticmethod
    def _get_purchased_course_ids(user_id: Optional[int]) -> set:
        """
        Множество id купленных курсов.
        MVP-1: покупок нет, всегда пусто.
        """
        return set()

    @staticmethod
    def _get_course_progress(user_id: int, course_id: int) -> dict:
        """Прогресс пользователя по курсу."""
        completed = (
            db.session.query(func.count(UserCourseProgress.id))
            .filter_by(user_id=user_id, course_id=course_id)
            .scalar()
        ) or 0
        total = (
            db.session.query(func.count(Lesson.id))
            .filter_by(course_id=course_id)
            .scalar()
        ) or 0
        return {"completed": int(completed), "total": int(total)}

    @staticmethod
    def _upsert_course_state(user_id: int, course_id: int, lesson_id: int) -> None:
        """Upsert UserCourseState при открытии урока."""
        now = datetime.now(timezone.utc)
        state = UserCourseState.query.filter_by(
            user_id=user_id, course_id=course_id
        ).first()
        if state is None:
            state = UserCourseState(
                user_id=user_id,
                course_id=course_id,
                last_viewed_lesson_id=lesson_id,
                started_at=now,
                last_viewed_at=now,
            )
            db.session.add(state)
        else:
            state.last_viewed_lesson_id = lesson_id
            state.last_viewed_at = now
        db.session.commit()

    @staticmethod
    def _recalc_lessons_count(course_id: int) -> None:
        """Пересчитывает денормализованный lessons_count."""
        count = (
            db.session.query(func.count(Lesson.id))
            .filter_by(course_id=course_id)
            .scalar()
        ) or 0
        db.session.query(Course).filter_by(id=course_id).update(
            {"lessons_count": int(count)}
        )
        db.session.commit()

    # ============================================================
    # КУРСЫ — ЧТЕНИЕ
    # ============================================================

    @staticmethod
    def list_courses(
        user_id: Optional[int] = None,
        *,
        category: Optional[str] = None,
        level: Optional[str] = None,
        is_free: Optional[bool] = None,
        search: str = "",
        page: int = 1,
        per_page: int = 12,
    ) -> dict:
        """
        Публичный список опубликованных курсов.
        """
        query = Course.query.filter(Course.status == ContentStatus.PUBLISHED)

        if category:
            query = query.filter(Course.category == category)
        if level:
            query = query.filter(Course.level == level)
        if is_free is not None:
            query = query.filter(Course.is_free == is_free)
        if search:
            like = f"%{search}%"
            query = query.filter(
                or_(Course.title.ilike(like), Course.short_description.ilike(like))
            )

        query = query.options(joinedload(Course.author)).order_by(
            Course.published_at.desc().nullslast(), Course.created_at.desc()
        )

        result = LearningService._paginate(query, page, per_page)
        purchased_ids = LearningService._get_purchased_course_ids(user_id)

        return {
            "courses": [
                LearningService._course_to_short(
                    c, is_purchased=(c.id in purchased_ids)
                )
                for c in result["items"]
            ],
            "pagination": result["pagination"],
        }

    @staticmethod
    def get_course_detail(user_id: Optional[int], course_slug: str) -> dict:
        """
        Публичная страница курса.
        Только опубликованные курсы.
        """
        course = (
            Course.query.options(
                selectinload(Course.lessons), joinedload(Course.author)
            )
            .filter(Course.slug == course_slug)
            .first()
        )
        if not course or course.status != ContentStatus.PUBLISHED:
            raise NotFoundError("Курс не найден")

        completed_ids = LearningService._get_completed_lesson_ids(user_id, course.id)
        is_purchased = course.id in LearningService._get_purchased_course_ids(user_id)

        last_viewed_lesson_id = None
        if user_id is not None:
            state = UserCourseState.query.filter_by(
                user_id=user_id, course_id=course.id
            ).first()
            if state is not None:
                last_viewed_lesson_id = state.last_viewed_lesson_id

        return LearningService._course_to_detail(
            course,
            user_id=user_id,
            completed_lesson_ids=completed_ids,
            is_purchased=is_purchased,
            last_viewed_lesson_id=last_viewed_lesson_id,
        )

    @staticmethod
    def admin_get_lesson(lesson_id: int) -> dict:
        lesson = db.session.get(Lesson, lesson_id)
        if not lesson:
            raise NotFoundError("Урок не найден")
        return {
            "id": lesson.id,
            "course_id": lesson.course_id,
            "title": lesson.title,
            "slug": lesson.slug,
            "order": lesson.order,
            "content": lesson.content,
            "video_url": lesson.video_url,
            "video_duration": lesson.video_duration,
            "is_free_preview": lesson.is_free_preview,
            "cover_url": lesson.cover_url,
        }

    # ============================================================
    # УРОКИ — ЧТЕНИЕ
    # ============================================================

    @staticmethod
    def get_lesson_detail(
        user_id: Optional[int], course_slug: str, lesson_slug: str
    ) -> dict:
        """
        Контент урока.

        Доступ:
        - курс опубликован
        - урок доступен пользователю (бесплатный курс / превью / покупка)
        Иначе — 403.

        Для авторизованного и доступного урока — upsert UserCourseState.
        """
        course = (
            Course.query.options(selectinload(Course.lessons))
            .filter(Course.slug == course_slug)
            .first()
        )
        if not course or course.status != ContentStatus.PUBLISHED:
            raise NotFoundError("Курс не найден")

        lesson = next((l for l in course.lessons if l.slug == lesson_slug), None)
        if lesson is None:
            raise NotFoundError("Урок не найден")

        if not LearningService.can_access_lesson(user_id, lesson):
            raise ForbiddenError("Для доступа к уроку необходимо купить курс")

        # Соседние уроки
        sorted_lessons = sorted(course.lessons, key=lambda l: (l.order, l.id))
        idx = next(i for i, l in enumerate(sorted_lessons) if l.id == lesson.id)
        prev_lesson = sorted_lessons[idx - 1] if idx > 0 else None
        next_lesson = sorted_lessons[idx + 1] if idx + 1 < len(sorted_lessons) else None

        def nav(l: Lesson) -> dict:
            return {
                "slug": l.slug,
                "title": l.title,
                "order": l.order,
                "is_accessible": LearningService.can_access_lesson(user_id, l),
            }

        is_completed = False
        if user_id is not None:
            is_completed = (
                db.session.query(UserCourseProgress.id)
                .filter_by(user_id=user_id, lesson_id=lesson.id)
                .first()
                is not None
            )
            LearningService._upsert_course_state(user_id, course.id, lesson.id)

        return {
            "id": lesson.id,
            "slug": lesson.slug,
            "order": lesson.order,
            "title": lesson.title,
            "content": lesson.content or "",
            "video_url": lesson.video_url,
            "video_duration": lesson.video_duration,
            "cover_url": lesson.cover_url,
            "is_free_preview": lesson.is_free_preview,
            "course_id": course.id,
            "course_slug": course.slug,
            "course_title": course.title,
            "is_completed": is_completed,
            "prev_lesson": nav(prev_lesson) if prev_lesson else None,
            "next_lesson": nav(next_lesson) if next_lesson else None,
        }

    # ============================================================
    # ПРОГРЕСС
    # ============================================================

    @staticmethod
    def complete_lesson(user_id: int, course_slug: str, lesson_slug: str) -> dict:
        """Отметить урок пройденным."""
        course = (
            Course.query.options(selectinload(Course.lessons))
            .filter(Course.slug == course_slug)
            .first()
        )
        if not course or course.status != ContentStatus.PUBLISHED:
            raise NotFoundError("Курс не найден")

        lesson = next((l for l in course.lessons if l.slug == lesson_slug), None)
        if lesson is None:
            raise NotFoundError("Урок не найден")

        if not LearningService.can_access_lesson(user_id, lesson):
            raise ForbiddenError("Для доступа к уроку необходимо купить курс")

        existing = UserCourseProgress.query.filter_by(
            user_id=user_id, lesson_id=lesson.id
        ).first()
        if existing is None:
            db.session.add(
                UserCourseProgress(
                    user_id=user_id,
                    course_id=course.id,
                    lesson_id=lesson.id,
                )
            )
            db.session.commit()

        return {
            "completed": True,
            "course_progress": LearningService._get_course_progress(user_id, course.id),
        }

    @staticmethod
    def uncomplete_lesson(user_id: int, course_slug: str, lesson_slug: str) -> dict:
        """Отменить отметку «пройдено»."""
        course = (
            Course.query.options(selectinload(Course.lessons))
            .filter(Course.slug == course_slug)
            .first()
        )
        if not course:
            raise NotFoundError("Курс не найден")

        lesson = next((l for l in course.lessons if l.slug == lesson_slug), None)
        if lesson is None:
            raise NotFoundError("Урок не найден")

        existing = UserCourseProgress.query.filter_by(
            user_id=user_id, lesson_id=lesson.id
        ).first()
        if existing is not None:
            db.session.delete(existing)
            db.session.commit()

        return {
            "completed": False,
            "course_progress": LearningService._get_course_progress(user_id, course.id),
        }

    # ============================================================
    # «МОЁ ОБУЧЕНИЕ»
    # ============================================================

    @staticmethod
    def get_my_learning(user_id: int) -> dict:
        """
        Три группы:
        - in_progress: есть state (начал смотреть) ИЛИ completed > 0, но не всё
        - completed: completed == total (total > 0)
        - not_started: доступен, но нет ни state, ни progress
        """
        # Все доступные курсы: бесплатные опубликованные + купленные
        purchased_ids = LearningService._get_purchased_course_ids(user_id)

        query = Course.query.options(
            selectinload(Course.lessons), joinedload(Course.author)
        ).filter(Course.status == ContentStatus.PUBLISHED)

        if purchased_ids:
            query = query.filter(
                or_(Course.is_free == True, Course.id.in_(purchased_ids))
            )
        else:
            query = query.filter(Course.is_free == True)

        courses = query.all()

        progress_rows = (
            db.session.query(
                UserCourseProgress.course_id,
                func.count(UserCourseProgress.id),
            )
            .filter_by(user_id=user_id)
            .group_by(UserCourseProgress.course_id)
            .all()
        )
        progress_by_course = {row[0]: int(row[1]) for row in progress_rows}

        # Состояния (что открывал)
        states = UserCourseState.query.filter_by(user_id=user_id).all()
        state_by_course = {s.course_id: s for s in states}

        # Уроки для last_viewed
        lesson_ids = [
            s.last_viewed_lesson_id
            for s in states
            if s.last_viewed_lesson_id is not None
        ]
        lessons_by_id = {}
        if lesson_ids:
            for l in Lesson.query.filter(Lesson.id.in_(lesson_ids)).all():
                lessons_by_id[l.id] = l

        in_progress: List[dict] = []
        completed_list: List[dict] = []
        not_started: List[dict] = []

        for course in courses:
            total = len(course.lessons)
            completed = progress_by_course.get(course.id, 0)
            state = state_by_course.get(course.id)

            last_slug = None
            last_title = None
            if state and state.last_viewed_lesson_id in lessons_by_id:
                last_lesson = lessons_by_id[state.last_viewed_lesson_id]
                last_slug = last_lesson.slug
                last_title = last_lesson.title

            item = {
                "course": LearningService._course_to_short(
                    course, is_purchased=(course.id in purchased_ids)
                ),
                "progress": {"completed": completed, "total": total},
                "last_viewed_lesson_slug": last_slug,
                "last_viewed_lesson_title": last_title,
            }

            if total > 0 and completed >= total:
                completed_list.append(item)
            elif state is not None or completed > 0:
                in_progress.append(item)
            else:
                not_started.append(item)

        return {
            "in_progress": in_progress,
            "completed": completed_list,
            "not_started": not_started,
        }

    # ============================================================
    # СТАТЬИ — ЧТЕНИЕ
    # ============================================================

    @staticmethod
    def list_articles(
        *,
        category: Optional[str] = None,
        tag: Optional[str] = None,
        search: str = "",
        page: int = 1,
        per_page: int = 12,
    ) -> dict:
        """Публичный список опубликованных статей."""
        query = Article.query.filter(Article.status == ContentStatus.PUBLISHED)

        if category:
            query = query.filter(Article.category == category)
        if tag:
            query = query.filter(func.cast(Article.tags, db.String).ilike(f'%"{tag}"%'))
        if search:
            like = f"%{search}%"
            query = query.filter(
                or_(Article.title.ilike(like), Article.short_description.ilike(like))
            )

        query = query.options(joinedload(Article.author)).order_by(
            Article.published_at.desc().nullslast(), Article.created_at.desc()
        )

        result = LearningService._paginate(query, page, per_page)
        return {
            "articles": [LearningService._article_to_short(a) for a in result["items"]],
            "pagination": result["pagination"],
        }

    @staticmethod
    def get_article_detail(article_slug: str) -> dict:
        """Публичная страница статьи + похожие."""
        article = (
            Article.query.options(joinedload(Article.author))
            .filter(Article.slug == article_slug)
            .first()
        )
        if not article or article.status != ContentStatus.PUBLISHED:
            raise NotFoundError("Статья не найдена")

        related = (
            Article.query.filter(
                Article.status == ContentStatus.PUBLISHED,
                Article.category == article.category,
                Article.id != article.id,
            )
            .order_by(Article.published_at.desc().nullslast())
            .limit(3)
            .all()
        )

        return LearningService._article_to_detail(article, related)

    # ============================================================
    # АДМИН — КУРСЫ
    # ============================================================

    @staticmethod
    def admin_list_courses(page: int = 1, per_page: int = 20) -> dict:
        """Список всех курсов для админки (включая черновики)."""
        query = Course.query.options(joinedload(Course.author)).order_by(
            Course.created_at.desc()
        )
        result = LearningService._paginate(query, page, per_page)
        return {
            "courses": [LearningService._course_to_short(c) for c in result["items"]],
            "pagination": result["pagination"],
        }

    @staticmethod
    def admin_get_course(course_id: int) -> dict:
        course = (
            Course.query.options(
                selectinload(Course.lessons), joinedload(Course.author)
            )
            .filter_by(id=course_id)
            .first()
        )
        if not course:
            raise NotFoundError("Курс не найден")

        data = LearningService._course_to_short(course)
        data.update(
            {
                "description": course.description,
                "status": course.status.value if course.status else None,
                "lessons": [
                    {
                        "id": l.id,
                        "slug": l.slug,
                        "order": l.order,
                        "title": l.title,
                        "is_free_preview": l.is_free_preview,
                        "has_video": bool(l.video_url),
                        "video_duration": l.video_duration,
                    }
                    for l in course.lessons
                ],
            }
        )
        return data

    @staticmethod
    def create_course(author_id: int, data: dict) -> Course:
        if Course.query.filter_by(slug=data["slug"]).first():
            raise ValidationError("Курс с таким slug уже существует")

        course = Course(
            author_id=author_id,
            title=data["title"],
            slug=data["slug"],
            description=data.get("description"),
            short_description=data.get("short_description"),
            category=data["category"],
            level=data.get("level", "beginner"),
            cover_url=data.get("cover_url"),
            price=data.get("price", 0),
            is_free=data.get("is_free", True),
            status=ContentStatus.DRAFT,
        )
        db.session.add(course)
        db.session.commit()
        return course

    @staticmethod
    def update_course(course_id: int, updates: dict) -> Course:
        course = db.session.get(Course, course_id)
        if not course:
            raise NotFoundError("Курс не найден")

        if "slug" in updates and updates["slug"] != course.slug:
            if Course.query.filter_by(slug=updates["slug"]).first():
                raise ValidationError("Курс с таким slug уже существует")

        for key, value in updates.items():
            if hasattr(course, key):
                setattr(course, key, value)

        # Синхронизация is_free с price
        course.is_free = course.price == 0

        db.session.commit()
        return course

    @staticmethod
    def delete_course(course_id: int) -> None:
        course = db.session.get(Course, course_id)
        if not course:
            raise NotFoundError("Курс не найден")
        db.session.delete(course)
        db.session.commit()

    @staticmethod
    def publish_course(course_id: int) -> Course:
        course = db.session.get(Course, course_id)
        if not course:
            raise NotFoundError("Курс не найден")
        if not course.lessons:
            raise ValidationError("Нельзя опубликовать курс без уроков")
        course.status = ContentStatus.PUBLISHED
        course.published_at = datetime.now(timezone.utc)
        db.session.commit()
        return course

    @staticmethod
    def archive_course(course_id: int) -> Course:
        course = db.session.get(Course, course_id)
        if not course:
            raise NotFoundError("Курс не найден")
        course.status = ContentStatus.ARCHIVED
        db.session.commit()
        return course

    # ============================================================
    # АДМИН — УРОКИ
    # ============================================================

    @staticmethod
    def create_lesson(course_id: int, data: dict) -> Lesson:
        course = db.session.get(Course, course_id)
        if not course:
            raise NotFoundError("Курс не найден")

        # Уникальность slug в рамках курса
        if Lesson.query.filter_by(course_id=course_id, slug=data["slug"]).first():
            raise ValidationError("Урок с таким slug уже существует в курсе")

        # order: если не передан — max + 1
        order = data.get("order")
        if order is None:
            max_order = (
                db.session.query(func.max(Lesson.order))
                .filter_by(course_id=course_id)
                .scalar()
            ) or 0
            order = max_order + 1

        # Уникальность order в рамках курса
        if Lesson.query.filter_by(course_id=course_id, order=order).first():
            raise ValidationError(f"Урок с order={order} уже существует")

        lesson = Lesson(
            course_id=course_id,
            title=data["title"],
            slug=data["slug"],
            order=order,
            content=data.get("content"),
            video_url=data.get("video_url"),
            video_duration=data.get("video_duration"),
            cover_url=data.get("cover_url"),
            is_free_preview=data.get("is_free_preview", False),
        )
        db.session.add(lesson)
        db.session.commit()

        LearningService._recalc_lessons_count(course_id)
        return lesson

    @staticmethod
    def update_lesson(lesson_id: int, updates: dict) -> Lesson:
        lesson = db.session.get(Lesson, lesson_id)
        if not lesson:
            raise NotFoundError("Урок не найден")

        if "slug" in updates and updates["slug"] != lesson.slug:
            if Lesson.query.filter_by(
                course_id=lesson.course_id, slug=updates["slug"]
            ).first():
                raise ValidationError("Урок с таким slug уже существует в курсе")

        if "order" in updates and updates["order"] != lesson.order:
            if Lesson.query.filter_by(
                course_id=lesson.course_id, order=updates["order"]
            ).first():
                raise ValidationError(f"Урок с order={updates['order']} уже существует")

        for key, value in updates.items():
            if hasattr(lesson, key):
                setattr(lesson, key, value)

        db.session.commit()
        return lesson

    @staticmethod
    def delete_lesson(lesson_id: int) -> None:
        lesson = db.session.get(Lesson, lesson_id)
        if not lesson:
            raise NotFoundError("Урок не найден")
        course_id = lesson.course_id
        db.session.delete(lesson)
        db.session.commit()
        LearningService._recalc_lessons_count(course_id)

    @staticmethod
    def reorder_lessons(course_id: int, items: List[dict]) -> None:
        """
        Переупорядочить уроки.
        items: [{id, order}, ...]
        """
        course = db.session.get(Course, course_id)
        if not course:
            raise NotFoundError("Курс не найден")

        # Проверка уникальности order в переданном наборе
        orders = [i["order"] for i in items]
        if len(orders) != len(set(orders)):
            raise ValidationError("order не может повторяться")

        for item in items:
            lesson = db.session.get(Lesson, item["id"])
            if not lesson or lesson.course_id != course_id:
                raise NotFoundError(f"Урок {item['id']} не найден в курсе")
            lesson.order = item["order"]

        db.session.commit()

    # ============================================================
    # АДМИН — СТАТЬИ
    # ============================================================

    @staticmethod
    def admin_list_articles(page: int = 1, per_page: int = 20) -> dict:
        query = Article.query.options(joinedload(Article.author)).order_by(
            Article.created_at.desc()
        )
        result = LearningService._paginate(query, page, per_page)
        return {
            "articles": [LearningService._article_to_short(a) for a in result["items"]],
            "pagination": result["pagination"],
        }

    @staticmethod
    def admin_get_article(article_id: int) -> dict:
        article = (
            Article.query.options(joinedload(Article.author))
            .filter_by(id=article_id)
            .first()
        )
        if not article:
            raise NotFoundError("Статья не найдена")
        data = LearningService._article_to_short(article)
        data.update(
            {
                "content": article.content,
                "status": article.status.value if article.status else None,
            }
        )
        return data

    @staticmethod
    def create_article(author_id: int, data: dict) -> Article:
        if Article.query.filter_by(slug=data["slug"]).first():
            raise ValidationError("Статья с таким slug уже существует")

        article = Article(
            author_id=author_id,
            title=data["title"],
            slug=data["slug"],
            short_description=data.get("short_description"),
            content=data["content"],
            category=data["category"],
            tags=data.get("tags", []),
            cover_url=data.get("cover_url"),
            status=ContentStatus.DRAFT,
        )
        db.session.add(article)
        db.session.commit()
        return article

    @staticmethod
    def update_article(article_id: int, updates: dict) -> Article:
        article = db.session.get(Article, article_id)
        if not article:
            raise NotFoundError("Статья не найдена")

        if "slug" in updates and updates["slug"] != article.slug:
            if Article.query.filter_by(slug=updates["slug"]).first():
                raise ValidationError("Статья с таким slug уже существует")

        for key, value in updates.items():
            if hasattr(article, key):
                setattr(article, key, value)

        db.session.commit()
        return article

    @staticmethod
    def delete_article(article_id: int) -> None:
        article = db.session.get(Article, article_id)
        if not article:
            raise NotFoundError("Статья не найдена")
        db.session.delete(article)
        db.session.commit()

    @staticmethod
    def publish_article(article_id: int) -> Article:
        article = db.session.get(Article, article_id)
        if not article:
            raise NotFoundError("Статья не найдена")
        article.status = ContentStatus.PUBLISHED
        article.published_at = datetime.now(timezone.utc)
        db.session.commit()
        return article

    @staticmethod
    def archive_article(article_id: int) -> Article:
        article = db.session.get(Article, article_id)
        if not article:
            raise NotFoundError("Статья не найдена")
        article.status = ContentStatus.ARCHIVED
        db.session.commit()
        return article
