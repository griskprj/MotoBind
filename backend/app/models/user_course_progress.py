from datetime import datetime, timezone

from app.extensions import db


class UserCourseProgress(db.Model):
    __tablename__ = "user_course_progress"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    course_id = db.Column(
        db.Integer,
        db.ForeignKey("courses.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    lesson_id = db.Column(
        db.Integer,
        db.ForeignKey("lessons.id", ondelete="CASCADE"),
        nullable=False,
    )

    completed_at = db.Column(
        db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
    )

    __table_args__ = (
        db.UniqueConstraint("user_id", "lesson_id", name="uq_user_lesson_progress"),
        db.Index("idx_user_course_progress", "user_id", "course_id"),
    )

    def __repr__(self):
        return f"<UserCourseProgress u={self.user_id} l={self.lesson_id}>"
