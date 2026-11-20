from datetime import datetime, timezone

from app.extensions import db
from app.models.learning_enums import ContentCategory, ContentStatus


class Article(db.Model):
    __tablename__ = "articles"

    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False, index=True
    )

    title = db.Column(db.String(128), nullable=False)
    slug = db.Column(db.String(128), unique=True, nullable=False, index=True)
    short_description = db.Column(db.String(256), nullable=True)

    content = db.Column(db.Text, nullable=False)

    category = db.Column(
        db.Enum(ContentCategory, name="content_category"),
        nullable=False,
        index=True,
    )
    tags = db.Column(db.JSON, nullable=True, default=list)

    cover_url = db.Column(db.String(256), nullable=True)

    status = db.Column(
        db.Enum(ContentStatus, name="content_status"),
        nullable=False,
        default=ContentStatus.DRAFT,
        index=True,
    )

    created_at = db.Column(
        db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
    )
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    published_at = db.Column(db.DateTime, nullable=True)

    author = db.relationship("User", backref="articles")

    __table_args__ = (
        db.Index("idx_article_status_category", "status", "category"),
        db.Index("idx_article_published_at", "published_at"),
    )

    def to_dict(self):
        return {
            "id": self.id,
            "author_id": self.author_id,
            "title": self.title,
            "slug": self.slug,
            "short_description": self.short_description,
            "content": self.content,
            "category": self.category.value if self.category else None,
            "tags": self.tags or [],
            "cover_url": self.cover_url,
            "status": self.status.value if self.status else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "published_at": self.published_at.isoformat()
            if self.published_at
            else None,
        }

    def __repr__(self):
        return f"<Article {self.slug}>"
