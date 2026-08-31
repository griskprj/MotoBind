from app.extensions import db
from app.models.notification import Notification
from app.exceptions import NotFoundError

class NotificationService:
    @staticmethod
    def send_notification(user_id, type, title, content, link=None, extra_data=None):
        notif = Notification(
            user_id=user_id,
            type=type,
            title=title,
            content=content,
            link=link,
            extra_data=extra_data,
        )
        db.session.add(notif)
        db.session.commit()
        return notif

    @staticmethod
    def get_user_notifications(user_id, page=1, per_page=20, unread_only=False):
        query = Notification.query.filter_by(user_id=user_id)
        if unread_only:
            query = query.filter_by(is_read=False)
        query = query.order_by(Notification.created_at.desc())
        paginated = query.paginate(page=page, per_page=per_page, error_out=False)
        return {
            'notifications': [n.to_dict() for n in paginated.items],
            'total': paginated.total,
            'pages': paginated.pages,
            'current_page': paginated.page,
            'per_page': paginated.per_page,
            'has_prev': paginated.has_prev,
            'has_next': paginated.has_next,
        }

    @staticmethod
    def mark_as_read(notification_id, user_id):
        notif = Notification.query.filter_by(id=notification_id, user_id=user_id).first()
        if not notif:
            raise NotFoundError('Уведомление не найдено')
        notif.is_read = True
        db.session.commit()
        return notif

    @staticmethod
    def mark_all_read(user_id):
        Notification.query.filter_by(user_id=user_id, is_read=False).update({'is_read': True})
        db.session.commit()

    @staticmethod
    def delete_notification(notification_id, user_id):
        notif = Notification.query.filter_by(id=notification_id, user_id=user_id).first()
        if not notif:
            raise NotFoundError('Уведомление не найдено')
        db.session.delete(notif)
        db.session.commit()

    @staticmethod
    def get_unread_count(user_id):
        return Notification.query.filter_by(user_id=user_id, is_read=False).count()