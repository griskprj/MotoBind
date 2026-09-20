"""
Response-схемы для домена social (posts, comments, likes, reports).
"""

from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict

from app.schemas.mixins import ISO8601Mixin

# ---------- Comments ----------


class CommentResponseSchema(ISO8601Mixin, BaseModel):
    """Ответ с одним комментарием."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    post_id: int
    user_id: int
    author: Optional[str] = None
    author_avatar: Optional[str] = None
    content: str
    created_at: Optional[datetime] = None


# ---------- Posts ----------


class PostResponseSchema(ISO8601Mixin, BaseModel):
    """
    Базовый ответ поста.

    Поля совпадают с Post.to_dict() + is_liked.
    """

    model_config = ConfigDict(from_attributes=True, extra="allow")

    id: int
    author_id: int
    author: Optional[str] = None
    author_avatar: Optional[str] = None
    content: str
    image: Optional[str] = None
    likes_count: int = 0
    comments_count: int = 0
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    is_liked: Optional[bool] = None


class PostDetailResponseSchema(PostResponseSchema):
    """Пост с вложенными комментариями (первые 5)."""

    comments: list[CommentResponseSchema] = []


class PostListResponseSchema(BaseModel):
    """Пагинированная лента постов."""

    posts: list[PostResponseSchema] = []
    total: int = 0
    pages: int = 0
    current_page: int = 1
    per_page: int = 20
    has_prev: bool = False
    has_next: bool = False


# ---------- Likes ----------


class LikeToggleResponseSchema(BaseModel):
    """Ответ POST /posts/<id>/like."""

    liked: bool
    likes_count: int


# ---------- Reports ----------


class ReportCategorySchema(BaseModel):
    """Одна категория жалобы."""

    value: str
    label: str


class ReportResponseSchema(ISO8601Mixin, BaseModel):
    """
    Ответ с жалобой (include_post=False).

    Поля совпадают с PostReport.to_dict(include_post=False).
    """

    model_config = ConfigDict(from_attributes=True)

    id: int
    post_id: Optional[int] = None
    reporter_id: int
    reporter: Optional[str] = None
    reporter_avatar: Optional[str] = None
    category: str
    category_label: Optional[str] = None
    description: Optional[str] = None
    status: str
    resolution_action: Optional[str] = None
    resolution_note: Optional[str] = None
    resolved_by: Optional[int] = None
    resolver: Optional[str] = None
    resolved_at: Optional[datetime] = None
    created_at: Optional[datetime] = None
    post_snapshot: Optional[dict[str, Any]] = None
