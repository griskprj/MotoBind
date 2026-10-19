from datetime import datetime
from typing import List, Optional

from app.models.learning_enums import ContentCategory
from app.schemas.learning_common import AuthorShortSchema, PaginationSchema
from pydantic import BaseModel, ConfigDict, Field

# ============================================================
# READING
# ============================================================


class ArticleShortSchema(BaseModel):
    """Статья в списке."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    slug: str
    title: str
    short_description: Optional[str] = None
    cover_url: Optional[str] = None
    category: ContentCategory
    tags: List[str] = Field(default_factory=list)
    author: Optional[AuthorShortSchema] = None
    created_at: Optional[datetime] = None
    published_at: Optional[datetime] = None


class ArticleDetailSchema(BaseModel):
    """Страница статьи — с контентом."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    slug: str
    title: str
    short_description: Optional[str] = None
    content: str
    cover_url: Optional[str] = None
    category: ContentCategory
    tags: List[str] = Field(default_factory=list)
    author: Optional[AuthorShortSchema] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    published_at: Optional[datetime] = None

    # Похожие статьи — заполняется сервисом
    related: List[ArticleShortSchema] = Field(default_factory=list)


class ArticleListResponseSchema(BaseModel):
    articles: List[ArticleShortSchema]
    pagination: PaginationSchema


# ============================================================
# ADMIN
# ============================================================


class ArticleCreateSchema(BaseModel):
    title: str = Field(..., min_length=1, max_length=128)
    slug: str = Field(..., min_length=1, max_length=128, pattern=r"^[a-z0-9_-]+$")
    short_description: Optional[str] = Field(None, max_length=256)

    content: str = Field(..., min_length=1)

    category: ContentCategory
    tags: List[str] = Field(default_factory=list)

    cover_url: Optional[str] = Field(None, max_length=256)

    model_config = {"str_strip_whitespace": True}


class ArticleUpdateSchema(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=128)
    slug: Optional[str] = Field(
        None, min_length=1, max_length=128, pattern=r"^[a-z0-9_-]+$"
    )
    short_description: Optional[str] = Field(None, max_length=256)

    content: Optional[str] = Field(None, min_length=1)

    category: Optional[ContentCategory] = None
    tags: Optional[List[str]] = None

    cover_url: Optional[str] = Field(None, max_length=256)

    model_config = {"str_strip_whitespace": True}

    def get_updates(self) -> dict:
        return self.model_dump(exclude_unset=True, exclude_none=True)
