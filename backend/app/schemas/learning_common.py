from typing import Generic, List, TypeVar

from pydantic import BaseModel, Field, computed_field

T = TypeVar("T")


class PaginationSchema(BaseModel):
    """Метаданные пагинации для списков."""

    total: int = Field(..., ge=0)
    page: int = Field(..., ge=1)
    per_page: int = Field(..., ge=1)
    pages: int = Field(..., ge=0)
    has_prev: bool
    has_next: bool


class PaginatedResponse(BaseModel, Generic[T]):
    """Обёртка над списком с пагинацией."""

    items: List[T]
    pagination: PaginationSchema


class AuthorShortSchema(BaseModel):
    """Краткая инфа об авторе контента."""

    model_config = {"from_attributes": True}

    id: int
    username: str


class CourseProgressSchema(BaseModel):
    """Прогресс по курсу."""

    completed: int = Field(..., ge=0)
    total: int = Field(..., ge=0)

    @computed_field
    @property
    def percent(self) -> int:
        if self.total == 0:
            return 0
        return round(self.completed / self.total * 100)

    @computed_field
    @property
    def is_completed(self) -> bool:
        return self.total > 0 and self.completed >= self.total
