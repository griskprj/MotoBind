from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

# ============================================================
# READING
# ============================================================


class LessonNavSchema(BaseModel):
    """Соседний урок для навигации."""

    slug: str
    title: str
    order: int
    is_accessible: bool = True


class LessonDetailSchema(BaseModel):
    """Страница урока — с контентом и навигацией."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    slug: str
    order: int
    title: str
    content: str
    video_url: Optional[str] = None
    video_duration: Optional[int] = None
    cover_url: Optional[str] = None
    is_free_preview: bool = False

    # Контекст курса
    course_id: int
    course_slug: str
    course_title: str

    # Прогресс (для авторизованного)
    is_completed: bool = False

    # Навигация
    prev_lesson: Optional[LessonNavSchema] = None
    next_lesson: Optional[LessonNavSchema] = None


LessonDetailSchema.model_rebuild()


# ============================================================
# ADMIN
# ============================================================


class LessonCreateSchema(BaseModel):
    title: str = Field(..., min_length=1, max_length=128)
    slug: str = Field(..., min_length=1, max_length=128, pattern=r"^[a-z0-9_-]+$")
    order: Optional[int] = Field(None, ge=1)

    content: str = Field(..., min_length=1)
    video_url: Optional[str] = Field(None, max_length=256)
    video_duration: Optional[int] = Field(None, ge=0)

    cover_url: Optional[str] = Field(None, max_length=256)
    is_free_preview: bool = False

    model_config = {"str_strip_whitespace": True}


class LessonUpdateSchema(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=128)
    slug: Optional[str] = Field(
        None, min_length=1, max_length=128, pattern=r"^[a-z0-9_-]+$"
    )
    order: Optional[int] = Field(None, ge=1)

    content: Optional[str] = Field(None, min_length=1)
    video_url: Optional[str] = Field(None, max_length=256)
    video_duration: Optional[int] = Field(None, ge=0)

    cover_url: Optional[str] = Field(None, max_length=256)
    is_free_preview: Optional[bool] = None

    model_config = {"str_strip_whitespace": True}

    def get_updates(self) -> dict:
        return self.model_dump(exclude_unset=True, exclude_none=True)


class LessonReorderItemSchema(BaseModel):
    id: int
    order: int = Field(..., ge=1)


class LessonReorderSchema(BaseModel):
    items: list[LessonReorderItemSchema] = Field(..., min_length=1)
