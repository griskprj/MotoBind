import os
from flask import current_app
from werkzeug.utils import secure_filename
from app.extensions import db
from app.models.user import User
from app.models.post import Post
from app.models.post_like import PostLike
from app.models.post_comment import PostComment
from app.exceptions import NotFoundError, ForbiddenError, ValidationError
from app.services.notification_service import NotificationService

class PostService:
    @staticmethod
    def create_post(author_id: int, content: str, image_file=None) -> Post:
        """Создаёт новый пост"""
        if not content or not content.strip():
            raise ValidationError("Содержимое поста не может быть пустым")

        image_path = None
        if image_file:
            image_path = PostService._save_image(image_file)

        post = Post(
            author_id=author_id,
            content=content.strip(),
            image=image_path
        )
        db.session.add(post)
        db.session.commit()
        return post

    @staticmethod
    def _save_image(file) -> str:
        """Сохраняет изображение поста"""
        from app.utils.files import compress_image
        
        allowed_extensions = {'jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp'}
        filename = file.filename.lower()
        if not any(filename.endswith(ext) for ext in allowed_extensions):
            raise ValidationError("Недопустимый формат изображения")

        try:
            compressed = compress_image(
                file,
                max_width=1920,
                quality=80,
                output_format="webp"
            )
            
            import uuid
            secure_name = secure_filename(f"post_{uuid.uuid4().hex[:8]}.webp")
            
            upload_dir = os.path.join(current_app.config["UPLOAD_FOLDER"], "posts")
            os.makedirs(upload_dir, exist_ok=True)
            
            filepath = os.path.join(upload_dir, secure_name)
            with open(filepath, 'wb') as f:
                f.write(compressed.getvalue())
            
            return f"posts/{secure_name}"
        except Exception as e:
            current_app.logger.error(f"Ошибка сохранения изображения поста: {e}")
            raise ValidationError("Не удалось сохранить изображение")

    @staticmethod
    def get_posts(page=1, per_page=20, user_id=None, current_user_id=None, include_comments=False):
        """Получает список постов с пагинацией"""
        query = Post.query
        
        if user_id:
            query = query.filter_by(author_id=user_id)
        
        query = query.order_by(Post.created_at.desc())
        paginated = query.paginate(page=page, per_page=per_page, error_out=False)
        
        posts_data = []
        for post in paginated.items:
            post_dict = post.to_dict(include_comments=include_comments)
            if current_user_id:
                like = PostLike.query.filter_by(post_id=post.id, user_id=current_user_id).first()
                post_dict['is_liked'] = bool(like)
            else:
                post_dict['is_liked'] = False
            posts_data.append(post_dict)
        
        return {
            'posts': posts_data,
            'total': paginated.total,
            'pages': paginated.pages,
            'current_page': paginated.page,
            'per_page': paginated.per_page,
            'has_prev': paginated.has_prev,
            'has_next': paginated.has_next,
        }

    @staticmethod
    def get_post(post_id: int, current_user_id=None, include_comments=False) -> dict:
        """Получает пост по ID с комментариями"""
        post = Post.query.get(post_id)
        if not post:
            raise NotFoundError("Пост не найден")
        
        post_dict = post.to_dict(include_comments=include_comments)
        
        if current_user_id:
            like = PostLike.query.filter_by(post_id=post.id, user_id=current_user_id).first()
            post_dict['is_liked'] = bool(like)
        
        return post_dict

    @staticmethod
    def update_post(post_id: int, user_id: int, content: str, image_file=None) -> Post:
        """Обновляет пост"""
        post = Post.query.get(post_id)
        if not post:
            raise NotFoundError("Пост не найден")
        
        if post.author_id != user_id:
            raise ForbiddenError("Вы можете редактировать только свои посты")

        if content and content.strip():
            post.content = content.strip()
        
        if image_file:
            if post.image:
                from app.utils.files import delete_file
                delete_file(post.image)
            post.image = PostService._save_image(image_file)
        else:
            pass
        
        db.session.commit()
        return post

    @staticmethod
    def delete_post(post_id: int, user_id: int) -> None:
        """Удаляет пост"""
        post = Post.query.get(post_id)
        if not post:
            raise NotFoundError("Пост не найден")
        
        if post.author_id != user_id:
            raise ForbiddenError("Вы можете удалять только свои посты")
        
        if post.image:
            from app.utils.files import delete_file
            delete_file(post.image)
        
        db.session.delete(post)
        db.session.commit()

    @staticmethod
    def toggle_like(post_id: int, user_id: int) -> dict:
        """Ставит/убирает лайк на посту"""
        post = Post.query.get(post_id)
        if not post:
            raise NotFoundError("Пост не найден")

        like = PostLike.query.filter_by(post_id=post_id, user_id=user_id).first()
        
        if like:
            db.session.delete(like)
            post.likes_count = max(0, post.likes_count - 1)
            liked = False
        else:
            like = PostLike(post_id=post_id, user_id=user_id)
            db.session.add(like)
            post.likes_count += 1
            liked = True
            
            if post.author_id != user_id:
                user = User.query.get(user_id)
                NotificationService.send_notification(
                    user_id=post.author_id,
                    type='social',
                    title='Новый лайк',
                    content=f'Пользователь {user.username} лайкнул ваш пост',
                    link=f'/social/post/{post_id}',
                    extra_data={'post_id': post_id, 'liked_by': user_id}
                )

        db.session.commit()
        return {'liked': liked, 'likes_count': post.likes_count}

    @staticmethod
    def add_comment(post_id: int, user_id: int, content: str) -> PostComment:
        """Добавляет комментарий к посту"""
        post = Post.query.get(post_id)
        if not post:
            raise NotFoundError("Пост не найден")

        if not content or not content.strip():
            raise ValidationError("Комментарий не может быть пустым")

        comment = PostComment(
            post_id=post_id,
            user_id=user_id,
            content=content.strip()
        )
        db.session.add(comment)
        post.comments_count += 1
        db.session.commit()

        if post.author_id != user_id:
            user = User.query.get(user_id)
            NotificationService.send_notification(
                user_id=post.author_id,
                type='social',
                title='Новый комментарий',
                content=f'Пользователь {user.username} прокомментировал ваш пост: {content[:50]}...',
                link=f'/social/post/{post_id}',
                extra_data={'post_id': post_id, 'comment_by': user_id, 'comment_id': comment.id}
            )

        return comment

    @staticmethod
    def delete_comment(comment_id: int, user_id: int) -> None:
        """Удаляет комментарий"""
        comment = PostComment.query.get(comment_id)
        if not comment:
            raise NotFoundError("Комментарий не найден")
        
        if comment.user_id != user_id:
            raise ForbiddenError("Вы можете удалять только свои комментарии")
        
        db.session.delete(comment)
        post = Post.query.get(comment.post_id)
        if post:
            post.comments_count = max(0, post.comments_count - 1)
        db.session.commit()