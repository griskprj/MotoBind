from datetime import datetime, timezone

from app.extensions import db


class Lesson(db.Model):
    __tablename__ = "lessons"

    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(
        db.Integer,
        db.ForeignKey("courses.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    order = db.Column(db.Integer, nullable=False, default=1, index=True)
    title = db.Column(db.String(128), nullable=False)
    slug = db.Column(db.String(128), nullable=False)

    content = db.Column(db.Text, nullable=True)
    video_url = db.Column(db.String(256), nullable=True)
    video_duration = db.Column(db.Integer, nullable=True)

    cover_url = db.Column(db.String(256), nullable=True)
    is_free_preview = db.Column(db.Boolean, default=False, nullable=False)

    created_at = db.Column(
        db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
    )
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    course = db.relationship("Course", back_populates="lessons")

    __table_args__ = (
        db.UniqueConstraint("course_id", "slug", name="uq_course_lesson_slug"),
        db.UniqueConstraint("course_id", "order", name="uq_course_lesson_order"),
        db.Index("idx_lesson_course_order", "course_id", "order"),
    )

    def to_dict(self):
        return {
            "id": self.id,
            "course_id": self.course_id,
            "order": self.order,
            "title": self.title,
            "slug": self.slug,
            "content": self.content,
            "video_url": self.video_url,
            "video_duration": self.video_duration,
            "cover_url": self.cover_url,
            "is_free_preview": self.is_free_preview,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

    def __repr__(self):
        return f"<Lesson {self.course_id}/{self.slug}>"
