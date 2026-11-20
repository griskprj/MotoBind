from datetime import datetime, timezone

from app.extensions import db


class UserCourseState(db.Model):
    __tablename__ = "user_course_states"

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
    last_viewed_lesson_id = db.Column(
        db.Integer,
        db.ForeignKey("lessons.id", ondelete="SET NULL"),
        nullable=True,
    )

    started_at = db.Column(
        db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
    )
    last_viewed_at = db.Column(
        db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
    )

    __table_args__ = (
        db.UniqueConstraint("user_id", "course_id", name="uq_user_course_state"),
    )

    def __repr__(self):
        return f"<UserCourseState u={self.user_id} c={self.course_id}>"
