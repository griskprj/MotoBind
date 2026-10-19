from typing import List, Optional

from app.schemas.course import CourseShortSchema
from app.schemas.learning_common import CourseProgressSchema
from pydantic import BaseModel


class CourseWithProgressSchema(BaseModel):
    """Курс + прогресс + последний урок."""

    course: CourseShortSchema
    progress: CourseProgressSchema
    last_viewed_lesson_slug: Optional[str] = None
    last_viewed_lesson_title: Optional[str] = None


class MyLearningResponseSchema(BaseModel):
    """Ответ /api/learning/my — три группы."""

    in_progress: List[CourseWithProgressSchema] = []
    completed: List[CourseWithProgressSchema] = []
    not_started: List[CourseWithProgressSchema] = []
