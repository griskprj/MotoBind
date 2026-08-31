import os
from typing import Any, Dict, List, Optional
from flask import current_app
from werkzeug.utils import secure_filename
from app.exceptions import ForbiddenError, NotFoundError
from app.extensions import db
from app.models.manual import Manual, ManualStep


class ManualService:
    """Сервис для работы с мануалами"""

    @staticmethod
    def create_manual(
        author_id: int,
        data: Dict[str, Any],
        files: Dict[str, Any] = None
    ) -> Manual:
        """Создает мануал с шагами и сохраняет изображения"""
        
        # Извлекаем данные
        title = data.get('title')
        description = data.get('description')
        category = data.get('category')
        difficult = data.get('difficult', 'easy')
        motorcycle = data.get('motorcycle')
        time_estimate = data.get('time_estimate')
        interval = data.get('interval')
        safety_tip = data.get('safety_tip')
        warnings = data.get('warnings')
        conditions = data.get('conditions')
        instruments = data.get('instruments')
        parts = data.get('parts')
        docs_links = data.get('docs_links')
        specs = data.get('specs')
        aftercare = data.get('aftercare')
        tip = data.get('tip')
        steps_data = data.get('steps', [])

        manual = Manual(
            author_id=author_id,
            title=title,
            description=description,
            category=category,
            difficult=difficult,
            motorcycle=motorcycle,
            time_estimate=time_estimate,
            interval=interval,
            safety_tip=safety_tip,
            warnings=warnings,
            conditions=conditions,
            docs_links=docs_links,
            specs=specs,
            aftercare=aftercare,
            instruments=instruments,
            parts=parts,
            tip=tip,
            status="moderate",
        )

        db.session.add(manual)
        db.session.flush()

        for idx, step_data in enumerate(steps_data):
            image_url = None
            if files:
                file_key = f'image_{idx + 1}'
                if file_key in files and files[file_key]:
                    image_url = ManualService._save_step_image(
                        files[file_key],
                        manual.id,
                        step_data.get('order', idx + 1)
                    )

            step = ManualStep(
                manual_id=manual.id,
                order=step_data.get('order', idx + 1),
                title=step_data.get('title'),
                text=step_data.get('text'),
                tip=step_data.get('tip'),
                warning=step_data.get('warning'),
                image=image_url,
                result=step_data.get('result'),
            )
            db.session.add(step)

        db.session.commit()
        return manual

    @staticmethod
    def _save_step_image(file, manual_id, step_order):
        """Сохраняет изображение шага в папку"""
        from app.utils.files import compress_image
        
        if not file:
            return None
        
        allowed_extensions = {'jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp'}
        filename = file.filename.lower()
        if not any(filename.endswith(ext) for ext in allowed_extensions):
            return None
        
        try:
            compressed = compress_image(
                file,
                max_width=1920,
                quality=80,
                output_format="webp"
            )
            
            secure_name = secure_filename(f"step_{manual_id}_{step_order}.webp")
            
            upload_dir = os.path.join(current_app.config["UPLOAD_FOLDER"], "manual_steps")
            os.makedirs(upload_dir, exist_ok=True)
            
            filepath = os.path.join(upload_dir, secure_name)
            
            with open(filepath, 'wb') as f:
                f.write(compressed.getvalue())
            
            return f"manual_steps/{secure_name}"
            
        except Exception as e:
            current_app.logger.error(f"Ошибка сохранения изображения: {e}")
            return None

    @staticmethod
    def update_manual(manual_id: int, user_id: int, is_admin=False, **kwargs) -> Manual:
        """Обновляет мануал"""
        manual = Manual.query.get(manual_id)
        if not manual:
            raise NotFoundError("Мануал не найден")

        if manual.author_id != user_id and not is_admin:
            raise ForbiddenError("Вы можете редактировать только свои мануалы")

        if manual.author_id == user_id:
            if manual.status == 'rejected':
                manual.status = 'moderate'
                manual.rejection_reason = None
            elif manual.status == 'approved':
                if not is_admin:
                    raise ForbiddenError("Нельзя редактировать опубликованный мануал. Обратитесь к администратору.")
            elif manual.status == 'moderate':
                if not is_admin:
                    raise ForbiddenError("Мануал уже на проверке, дождитесь решения администратора.")
        else:
            if not is_admin:
                raise ForbiddenError("Вы не являетесь автором этого мануала")

        if "steps" in kwargs:
            steps_data = kwargs.pop("steps")
            ManualService._update_steps(manual.id, steps_data)

        for key, value in kwargs.items():
            if hasattr(manual, key) and value is not None:
                setattr(manual, key, value)

        db.session.commit()
        return manual

    @staticmethod
    def _update_steps(manual_id: int, steps_data: List[Dict[str, Any]]) -> None:
        """Обновляет шаги мануала"""
        ManualStep.query.filter_by(manual_id=manual_id).delete()

        for step_data in steps_data:
            step = ManualStep(
                manual_id=manual_id,
                order=step_data["order"],
                title=step_data["title"],
                text=step_data.get("text"),
                tip=step_data.get("tip"),
                warning=step_data.get("warning"),
                image=step_data.get("image"),
                result=step_data.get("result"),
            )
            db.session.add(step)

    @staticmethod
    def get_manual(manual_id: int, user_id: Optional[int] = None) -> Manual:
        """Получает мануал с проверкой прав"""
        manual = Manual.query.get(manual_id)
        if not manual:
            raise NotFoundError("Мануал не найден")
        
        if user_id is not None and manual.author_id != user_id:
            raise ForbiddenError("У вас нет доступа к этому мануалу")
        
        return manual

    @staticmethod
    def delete_manual(manual_id: int, user_id: int) -> None:
        """Удаляет мануал"""
        manual = Manual.query.get(manual_id)
        if not manual:
            raise NotFoundError("Мануал не найден")

        if manual.author_id != user_id:
            raise ForbiddenError("Вы можете удалять только свои мануалы")

        db.session.delete(manual)
        db.session.commit()

    @staticmethod
    def get_manual_for_maintenance(
        maintenance_title: str,
        motorcycle_name: str,
        user_id: int
    ) -> Optional[Manual]:
        """Находит подходящий мануал для обслуживания"""
        import re
        
        search_words = re.findall(r"\w+", maintenance_title.lower())
        
        if not search_words:
            return None
        
        conditions = [Manual.title.ilike(f"%{word}%") for word in search_words]
        manuals_found = Manual.query.filter(
            Manual.motorcycle.ilike(f"%{motorcycle_name}%"),
            *conditions,
            Manual.status == "approved"
        ).all()
        
        if not manuals_found:
            from sqlalchemy import or_
            manuals_found = Manual.query.filter(
                Manual.motorcycle.ilike(f"%{motorcycle_name}%"),
                or_(*conditions),
                Manual.status == "approved"
            ).all()
        
        if not manuals_found:
            brand = motorcycle_name.split()[0] if motorcycle_name.split() else motorcycle_name
            manuals_found = Manual.query.filter(
                Manual.motorcycle.ilike(f"%{brand}%"),
                or_(*conditions),
                Manual.status == "approved"
            ).all()
        
        if not manuals_found:
            return None
        
        manual = max(
            manuals_found,
            key=lambda m: sum(
                1 for word in search_words
                if word.lower() in m.title.lower()
            )
        )
        
        return manual