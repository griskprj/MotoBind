# notifications.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.notification_service import NotificationService
from app.exceptions import NotFoundError
from app.services.push_service import PushService

notifications_bp = Blueprint('notifications', __name__)


@notifications_bp.route('/push/config', methods=['GET'])
@jwt_required()
def get_push_config():
    return jsonify(PushService.public_config(int(get_jwt_identity()))), 200


@notifications_bp.route('/push/subscriptions', methods=['POST'])
@jwt_required()
def save_push_subscription():
    data = request.get_json(silent=True) or {}
    subscription = PushService.save_subscription(int(get_jwt_identity()), data)
    return jsonify({'message': 'Push-уведомления включены', 'id': subscription.id}), 201


@notifications_bp.route('/push/subscriptions', methods=['DELETE'])
@jwt_required()
def remove_push_subscription():
    data = request.get_json(silent=True) or {}
    endpoint = data.get('endpoint')
    removed = PushService.remove_subscription(
        int(get_jwt_identity()), str(endpoint) if endpoint else None
    )
    return jsonify({'message': 'Push-уведомления отключены', 'removed': removed}), 200


@notifications_bp.route('/', methods=['GET'])
@jwt_required()
def get_notifications():
    user_id = int(get_jwt_identity())
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    unread_only = request.args.get('unread_only', 'false').lower() == 'true'
    data = NotificationService.get_user_notifications(user_id, page, per_page, unread_only)
    return jsonify(data), 200


@notifications_bp.route('/unread-count', methods=['GET'])
@jwt_required()
def unread_count():
    user_id = int(get_jwt_identity())
    count = NotificationService.get_unread_count(user_id)
    return jsonify({'unread_count': count}), 200


@notifications_bp.route('/<int:notification_id>/read', methods=['PUT'])
@jwt_required()
def mark_read(notification_id):
    user_id = int(get_jwt_identity())
    try:
        notif = NotificationService.mark_as_read(notification_id, user_id)
        return jsonify(notif.to_dict()), 200
    except NotFoundError as e:
        return jsonify({'error': str(e)}), 404


@notifications_bp.route('/read-all', methods=['PUT'])
@jwt_required()
def mark_all_read():
    user_id = int(get_jwt_identity())
    NotificationService.mark_all_read(user_id)
    return jsonify({'message': 'Все уведомления отмечены как прочитанные'}), 200


@notifications_bp.route('/<int:notification_id>', methods=['DELETE'])
@jwt_required()
def delete_notification(notification_id):
    user_id = int(get_jwt_identity())
    try:
        NotificationService.delete_notification(notification_id, user_id)
        return jsonify({'message': 'Уведомление удалено'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 404
