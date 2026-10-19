from datetime import datetime, timezone

from app.extensions import db
from app.models.learning_enums import ContentCategory, ContentStatus, CourseLevel


class Course(db.Model):
    __tablename__ = "courses"

    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False, index=True
    )

    title = db.Column(db.String(128), nullable=False)
    slug = db.Column(db.String(128), unique=True, nullable=False, index=True)
    description = db.Column(db.Text, nullable=True)
    short_description = db.Column(db.String(256), nullable=True)

    category = db.Column(
        db.Enum(ContentCategory, name="content_category"),
        nullable=False,
        index=True,
    )
    level = db.Column(
        db.Enum(CourseLevel, name="course_level"),
        nullable=False,
        default=CourseLevel.BEGINNER,
        index=True,
    )

    cover_url = db.Column(db.String(256), nullable=True)

    price = db.Column(db.Integer, nullable=False, default=0)  # копейки
    is_free = db.Column(db.Boolean, default=True, nullable=False, index=True)

    status = db.Column(
        db.Enum(ContentStatus, name="content_status"),
        nullable=False,
        default=ContentStatus.DRAFT,
        index=True,
    )

    lessons_count = db.Column(db.Integer, default=0, nullable=False)

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

    # Связи
    author = db.relationship("User", backref="courses")
    lessons = db.relationship(
        "Lesson",
        back_populates="course",
        order_by="Lesson.order, Lesson.id",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    __table_args__ = (
        db.Index("idx_course_status_category", "status", "category"),
        db.Index("idx_course_published_at", "published_at"),
    )

    def to_dict(self):
        """Базовое представление (для админки и сервисов)."""
        return {
            "id": self.id,
            "author_id": self.author_id,
            "title": self.title,
            "slug": self.slug,
            "description": self.description,
            "short_description": self.short_description,
            "category": self.category.value if self.category else None,
            "level": self.level.value if self.level else None,
            "cover_url": self.cover_url,
            "price": self.price,
            "is_free": self.is_free,
            "status": self.status.value if self.status else None,
            "lessons_count": self.lessons_count,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "published_at": self.published_at.isoformat()
            if self.published_at
            else None,
        }

    def __repr__(self):
        return f"<Course {self.slug}>"
