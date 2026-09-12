from datetime import datetime, timezone
from app.extensions import db
from app.exceptions import (
    ConflictError,
    NotFoundError,
    ValidationError
)
from app.models.post import Post
from app.models.post_report import PostReport
from app.models.user import User
from app.services.notification_service import NotificationService


class ReportService:

    @staticmethod
    def create_report(post_id: int, reporter_id: int, category: str, description: str | None = None) -> PostReport:
        post = Post.query.get(post_id)
        if not post:
            raise NotFoundError("Пост не найден")

        if post.author_id == reporter_id:
            raise ValidationError("Нельзя жаловаться на свой пост")

        if category not in PostReport.CATEGORIES:
            raise ValidationError("Неверная категория жалобы")

        existing = PostReport.query.filter_by(
            post_id=post_id,
            reporter_id=reporter_id,
            status="pending",
        ).first()
        if existing:
            raise ConflictError("Вы уже отправили жалобу на этот пост")

        shapshot = {
            "content": post.content,
            "image": post.image,
            "author_id": post.author_id,
            "author": post.author.username if post.author else None,
            "author_avatar": post.author.avatar if post.author else None,
            "craeted_at": post.created_at.isoformat()+ "Z" if post.created_at else None
        }

        report = PostReport(
            post_id=post_id,
            reporter_id=reporter_id,
            category=category,
            description=(description or "").strip() or None,
            post_snapshot=shapshot,
        )
        db.session.add(report)
        db.session.commit()
        return report

    @staticmethod
    def get_reports(page=1, per_page=20, status=None, category=None):
        query = PostReport.query

        if status:
            query = query.filter_by(status=status)
        if category:
            query = query.filter_by(category=category)

        query = query.order_by(PostReport.created_at.desc())
        paginated = query.paginate(page=page, per_page=per_page, error_out=False)

        return {
            "reports": [r.to_dict() for r in paginated.items],
            "total": paginated.total,
            "pages": paginated.pages,
            "current_page": paginated.page,
            "current_page": paginated.page,
            "per_page": paginated.per_page,
            "has_prev": paginated.has_prev,
            "has_next": paginated.has_next,
            "stats": {
                "total": PostReport.query.count(),
                "pending": PostReport.query.filter_by(status="pending").count(),
                "resolved": PostReport.query.filter_by(status="resolved").count(),
                "rejected": PostReport.query.filter_by(status="rejected").count(),
            },
        }

    @staticmethod
    def resolve_report(report_id: int, admin_id: int, action: str, note: str | None = None) -> PostReport:
        report = PostReport.query.get(report_id)
        if not report:
            raise NotFoundError("Жалоба не найдена")
        if report.status != "pending":
            raise ValidationError("Жалоба уже рассмотрена")
        if action not in ("post_deleted", "user_banned", "both"):
            raise ValidationError("Неверное действие")

        post = Post.query.get(report.post_id) if report.post_id else None
        author_id = post.author_id if post else (report.post_snapshot or {}).get("author_id")

        if action in ("post_deleted", "both") and post:
            if post.image:
                from app.utils.files import delete_file
                delete_file(post.image)
            db.session.delete(post)

        if action in ("user_banned", "both") and author_id:
            author = User.query.get(author_id)
            if author and author.status != "banned" and author.id != admin_id:
                author.status = "banned"
                NotificationService.send_notification(
                    user_id=author.id,
                    type="moderation",
                    title="Ваш аккаунт заблокирован",
                    content="Ваш аккаунт был заблокирован за нарушение правил сообщества.",
                    link=None,
                )

        report.status = "resolved"
        report.resolution_action = action
        report.resolution_note = (note or "").strip() or None
        report.resolved_by = admin_id
        report.resolved_at = datetime.now(timezone.utc)

        db.session.commit()

        NotificationService.send_notification(
            user_id=report.reporter_id,
            type="report_status",
            title="Ваша жалоба рассмотрена",
            content="Спасибо за помощь! Модератор принял меры по вашей жалобе.",
            link=f"/social/post/{report.post_id}" if report.post_id else None,
            extra_data={"report_id": report.id, "action": action},
        )

        return report

    @staticmethod
    def reject_report(report_id: int, admin_id: int, note: str | None = None) -> PostReport:
        report = PostReport.query.get(report_id)
        if not report:
            raise NotFoundError("Жалоба не найдена")
        if report.status != "pending":
            raise ValidationError("Жалоба уже рассмотрена")

        report.status = "rejected"
        report.resolution_action = "none"
        report.resolution_note = (note or "").strip() or None
        report.resolved_by = admin_id
        report.resolved_at = datetime.now(timezone.utc)
        db.session.commit()
        return report