from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.post_service import PostService
from app.exceptions import NotFoundError, ForbiddenError, ValidationError

social_bp = Blueprint('social', __name__)

@social_bp.route('/posts', methods=['POST'])
@jwt_required()
def create_post():
    """Создание поста"""
    try:
        user_id = int(get_jwt_identity())
        content = request.form.get('content')
        image = request.files.get('image')
        
        if not content or not content.strip():
            return jsonify({'error': 'Содержимое поста не может быть пустым'}), 400
        
        post = PostService.create_post(user_id, content, image)
        return jsonify(post.to_dict()), 201
    except ValidationError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@social_bp.route('/posts', methods=['GET'])
@jwt_required()
def get_posts():
    """Получение списка постов"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    user_id = request.args.get('user_id', type=int)
    include_comments = request.args.get('include_comments', 'false').lower() == 'true'
    
    data = PostService.get_posts(page, per_page, user_id, include_comments)
    return jsonify(data), 200

@social_bp.route('/posts/<int:post_id>', methods=['GET'])
@jwt_required()
def get_post(post_id):
    """Получение поста по ID"""
    try:
        include_comments = request.args.get('include_comments', 'true').lower() == 'true'
        post = PostService.get_post(post_id, include_comments)
        return jsonify(post.to_dict(include_comments=include_comments)), 200
    except NotFoundError as e:
        return jsonify({'error': str(e)}), 404

@social_bp.route('/posts/<int:post_id>', methods=['PUT'])
@jwt_required()
def update_post(post_id):
    """Обновление поста"""
    try:
        user_id = int(get_jwt_identity())
        content = request.form.get('content')
        image = request.files.get('image')
        
        post = PostService.update_post(post_id, user_id, content, image)
        return jsonify(post.to_dict()), 200
    except (NotFoundError, ForbiddenError, ValidationError) as e:
        return jsonify({'error': str(e)}), 400 if isinstance(e, ValidationError) else 403 if isinstance(e, ForbiddenError) else 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@social_bp.route('/posts/<int:post_id>', methods=['DELETE'])
@jwt_required()
def delete_post(post_id):
    """Удаление поста"""
    try:
        user_id = int(get_jwt_identity())
        PostService.delete_post(post_id, user_id)
        return jsonify({'message': 'Пост удалён'}), 200
    except (NotFoundError, ForbiddenError) as e:
        return jsonify({'error': str(e)}), 404 if isinstance(e, NotFoundError) else 403

@social_bp.route('/posts/<int:post_id>/like', methods=['POST'])
@jwt_required()
def toggle_like(post_id):
    """Поставить/убрать лайк"""
    try:
        user_id = int(get_jwt_identity())
        result = PostService.toggle_like(post_id, user_id)
        return jsonify(result), 200
    except NotFoundError as e:
        return jsonify({'error': str(e)}), 404

@social_bp.route('/posts/<int:post_id>/comments', methods=['POST'])
@jwt_required()
def add_comment(post_id):
    """Добавить комментарий"""
    try:
        user_id = int(get_jwt_identity())
        data = request.get_json()
        if not data or not data.get('content'):
            return jsonify({'error': 'Комментарий не может быть пустым'}), 400
        
        comment = PostService.add_comment(post_id, user_id, data['content'])
        return jsonify(comment.to_dict()), 201
    except (NotFoundError, ValidationError) as e:
        return jsonify({'error': str(e)}), 404 if isinstance(e, NotFoundError) else 400

@social_bp.route('/comments/<int:comment_id>', methods=['DELETE'])
@jwt_required()
def delete_comment(comment_id):
    """Удалить комментарий"""
    try:
        user_id = int(get_jwt_identity())
        PostService.delete_comment(comment_id, user_id)
        return jsonify({'message': 'Комментарий удалён'}), 200
    except (NotFoundError, ForbiddenError) as e:
        return jsonify({'error': str(e)}), 404 if isinstance(e, NotFoundError) else 403