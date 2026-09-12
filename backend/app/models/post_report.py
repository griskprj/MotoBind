from datetime import datetime, timezone
from app.extensions import db


class PostReport(db.Model):
    """Жалоба на пост"""
    __tablename__ = "post_reports"

    id = db.Column(db.Integer, primary_key=True)

    post_id = db.Column(
        db.Integer,
        db.ForeignKey("posts.id", ondelete="SET NULL"),
        nullable=True,
    )

    post_snapshot = db.Column(db.JSON, nullable=True)

    reporter_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    category = db.Column(db.String(64), nullable=False)
    description = db.Column(db.Text, nullable=True)

    status = db.Column(db.String(32), default="pending", nullable=False)

    resolution_action = db.Column(db.String(32), nullable=True)
    resolution_note = db.Column(db.Text, nullable=True)
    resolved_by = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )
    resolved_at = db.Column(db.DateTime, nullable=True)

    created_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    post = db.relationship("Post", foreign_keys=[post_id])
    reporter = db.relationship("User", foreign_keys=[reporter_id])
    resolver = db.relationship("User", foreign_keys=[resolved_by])

    CATEGORIES = {
        "sexual_content": "Контент сексуального характера",
        "hate_speech": "Разжигание межнациональной розни",
        "extremism": "Экстремистская символика",
        "violence": "Насилие и жестокость",
        "drugs": "Пропаганда наркотиков",
        "spam": "Спам и мошенничество",
        "other": "Другое",
    }

    def to_dict(self, include_post=True):
        data = {
            "id": self.id,
            "post_id": self.post_id,
            "reporter_id": self.reporter_id,
            "reporter": self.reporter.username if self.reporter else None,
            "reporter_avatar": self.reporter.avatar if self.reporter else None,
            "category": self.category,
            "category_label": self.CATEGORIES.get(self.category, self.category),
            "description": self.description,
            "status": self.status,
            "resolution_action": self.resolution_action,
            "resolution_note": self.resolution_note,
            "resolved_by": self.resolved_by,
            "resolver": self.resolver.username if self.resolver else None,
            "resolved_at": self.resolved_at.isoformat() + "Z" if self.resolved_at else None,
            "created_at": self.created_at.isoformat() + "Z" if self.created_at else None,
            "post_snapshot": self.post_snapshot,
        }

        if include_post:
            if self.post:
                data["post"] = {
                    "id": self.post.id,
                    "content": self.post.content,
                    "image": self.post.image,
                    "author_id": self.post.author_id,
                    "author": self.post.author.username if self.post.author else None,
                    "author_avatar": self.post.author.avatar if self.post.author else None,
                    "created_at": self.post.created_at.isoformat() + "Z" if self.post.created_at else None,
                    "is_deleted": False,
                }
            elif self.post_snapshot:
                data["post"] = {**self.post_snapshot, "is_deleted": True}
            else:
                data["post"] = None

        return data