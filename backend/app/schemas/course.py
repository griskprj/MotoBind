from datetime import datetime
from typing import List, Optional

from app.models.learning_enums import ContentCategory, CourseLevel
from app.schemas.learning_common import (
    AuthorShortSchema,
    CourseProgressSchema,
    PaginationSchema,
)
from pydantic import BaseModel, ConfigDict, Field, field_validator

# ============================================================
# READING — публичные
# ============================================================


class CourseShortSchema(BaseModel):
    """Курс в списке."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    slug: str
    title: str
    short_description: Optional[str] = None
    cover_url: Optional[str] = None
    category: ContentCategory
    level: CourseLevel
    price: int = 0
    is_free: bool = True
    lessons_count: int = 0
    author: Optional[AuthorShortSchema] = None
    created_at: Optional[datetime] = None
    published_at: Optional[datetime] = None

    # Заполняется сервисом для авторизованного
    is_purchased: bool = False


class LessonShortSchema(BaseModel):
    """Урок в программе курса — без content."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    slug: str
    order: int
    title: str
    is_free_preview: bool = False
    has_video: bool = False
    video_duration: Optional[int] = None

    # Заполняется сервисом для авторизованного
    is_completed: bool = False
    is_accessible: bool = True


class CourseDetailSchema(BaseModel):
    """Страница курса — с программой и прогрессом."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    slug: str
    title: str
    description: Optional[str] = None
    short_description: Optional[str] = None
    cover_url: Optional[str] = None
    category: ContentCategory
    level: CourseLevel
    price: int = 0
    is_free: bool = True
    lessons_count: int = 0
    author: Optional[AuthorShortSchema] = None
    created_at: Optional[datetime] = None
    published_at: Optional[datetime] = None

    # Заполняется сервисом
    is_purchased: bool = False
    lessons: List[LessonShortSchema] = Field(default_factory=list)
    progress: Optional[CourseProgressSchema] = None
    last_viewed_lesson_id: Optional[int] = None


class CourseListResponseSchema(BaseModel):
    """Ответ списка курсов с пагинацией."""

    courses: List[CourseShortSchema]
    pagination: PaginationSchema


# ============================================================
# ADMIN — создание / обновление
# ============================================================


class CourseCreateSchema(BaseModel):
    title: str = Field(..., min_length=1, max_length=128)
    slug: str = Field(..., min_length=1, max_length=128, pattern=r"^[a-z0-9_-]+$")
    description: Optional[str] = None
    short_description: Optional[str] = Field(None, max_length=256)

    category: ContentCategory
    level: CourseLevel = CourseLevel.BEGINNER

    cover_url: Optional[str] = Field(None, max_length=256)

    price: int = Field(0, ge=0)
    is_free: bool = True

    model_config = {"str_strip_whitespace": True}

    @field_validator("is_free", mode="after")
    @classmethod
    def sync_is_free(cls, v, info):
        price = info.data.get("price", 0)
        return price == 0


class CourseUpdateSchema(BaseModel):
    """Все поля опциональны — PATCH-семантика."""

    title: Optional[str] = Field(None, min_length=1, max_length=128)
    slug: Optional[str] = Field(
        None, min_length=1, max_length=128, pattern=r"^[a-z0-9_-]+$"
    )
    description: Optional[str] = None
    short_description: Optional[str] = Field(None, max_length=256)

    category: Optional[ContentCategory] = None
    level: Optional[CourseLevel] = None

    cover_url: Optional[str] = Field(None, max_length=256)

    price: Optional[int] = Field(None, ge=0)
    is_free: Optional[bool] = None

    model_config = {"str_strip_whitespace": True}

    def get_updates(self) -> dict:
        return self.model_dump(exclude_unset=True, exclude_none=True)
