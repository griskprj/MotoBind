from flask import current_app
from sqlalchemy import or_
from typing import Any, Dict, List, Optional
from werkzeug.utils import secure_filename
import os

from app.exceptions import ForbiddenError, NotFoundError
from app.extensions import db
from app.models.manual import Manual, ManualStep
from app.models.motorcycle import Motorcycle
from app.models.user import User


class ManualService:
    """Сервис для работы с мануалами"""

    @staticmethod
    def list_manuals(
        user_id: int,
        page: int = 1,
        per_page: int = 8,
        tab: str = "all",
        search: str = "",
        motorcycle_filter: str = "",
        category: str = "",
        sort_by: str = "created_at_desc",
        difficult: str = "",
        time_estimate: str = "",
        interval: str = "",
        status: str = "",
    ) -> dict:
        """
        Возвращает пагинированный список мануалов с фильтрами.

        Возвращает dict для API (без response-схемы, контракт сохранён).
        """

        query = Manual.query

        if tab == "my":
            query = query.filter(Manual.author_id == user_id)
        elif tab == "myMotos":
            user_motorcycles = Motorcycle.query.filter_by(owner_id=user_id).all()
            moto_names = [moto.name for moto in user_motorcycles]
            if moto_names:
                query = query.filter(Manual.motorcycle.in_(moto_names))
            else:
                return {
                    "manuals": [],
                    "total": 0,
                    "pages": 0,
                    "current_page": page,
                    "per_page": per_page,
                    "has_prev": False,
                    "has_next": False,
                }

        if search:
            query = query.filter(
                or_(
                    Manual.title.ilike(f"%{search}%"),
                    Manual.motorcycle.ilike(f"%{search}%"),
                    Manual.description.ilike(f"%{search}%"),
                    Manual.author.has(User.username.ilike(f"%{search}%")),
                )
            )

        if motorcycle_filter:
            query = query.filter(Manual.motorcycle.ilike(f"%{motorcycle_filter}%"))

        if category:
            query = query.filter(Manual.category == category)

        if difficult:
            query = query.filter(Manual.difficult == difficult)

        if time_estimate:
            query = query.filter(Manual.time_estimate.ilike(f"%{time_estimate}%"))

        if interval:
            query = query.filter(Manual.interval.ilike(f"%{interval}%"))

        if status:
            current_user = db.session.get(User, user_id)
            if current_user is not None and current_user.role == "admin":
                query = query.filter(Manual.status == status)

        sort_mapping = {
            "created_at_desc": Manual.created_at.desc(),
            "created_at_asc": Manual.created_at.asc(),
            "title_asc": Manual.title.asc(),
            "title_desc": Manual.title.desc(),
            "difficult_asc": Manual.difficult.asc(),
            "difficult_desc": Manual.difficult.desc(),
        }
        query = query.order_by(sort_mapping.get(sort_by, Manual.created_at.desc()))

        paginated = query.paginate(page=page, per_page=per_page, error_out=False)

        return {
            "manuals": [m.to_dict() for m in paginated.items],
            "total": paginated.total,
            "pages": paginated.pages,
            "current_page": paginated.page,
            "per_page": paginated.per_page,
            "has_prev": paginated.has_prev,
            "has_next": paginated.has_next,
        }

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
    def update_manual(manual_id: int, user_id: int, **kwargs) -> Manual:
        """
        Обновляет мануал.

        is_admin определяется внутри — сервис сам проверяет роль пользователя.
        """
        from app.models.user import User

        manual = db.session.get(Manual, manual_id)
        if not manual:
            raise NotFoundError("Мануал не найден")

        user = db.session.get(User, user_id)
        is_admin = user is not None and user.role == "admin"

        if manual.author_id != user_id and not is_admin:
            raise ForbiddenError("Вы можете редактировать только свои мануалы")

        if manual.author_id == user_id:
            if manual.status == "rejected":
                manual.status = "moderate"
                manual.rejection_reason = None
            elif manual.status == "approved":
                if not is_admin:
                    raise ForbiddenError("Нельзя редактировать опубликованный мануал. Обратитесь к администратору.")
            elif manual.status == "moderate":
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
        """Обновляет шаги мануала, сохраняя существующие картинки."""
        existing_steps = {
            s.order: s for s in ManualStep.query.filter_by(manual_id=manual_id).all()
        }

        new_orders = {step_data["order"] for step_data in steps_data}
        for order, old_step in existing_steps.items():
            if order not in new_orders:
                db.session.delete(old_step)

        for step_data in steps_data:
            order = step_data["order"]
            if order in existing_steps:
                step = existing_steps[order]
                step.title = step_data["title"]
                step.text = step_data.get("text")
                step.tip = step_data.get("tip")
                step.warning = step_data.get("warning")
                step.result = step_data.get("result")
            else:
                step = ManualStep(
                    manual_id=manual_id,
                    order=order,
                    title=step_data["title"],
                    text=step_data.get("text"),
                    tip=step_data.get("tip"),
                    warning=step_data.get("warning"),
                    result=step_data.get("result"),
                )
                db.session.add(step)

    @staticmethod
    def get_manual_for_user(manual_id: int, user_id: int) -> Manual:
        """
        Возвращает мануал с проверкой доступа.

        Approved видят все.
        Moderate/rejected — только автор и админ.
        """
        from app.models.user import User

        manual = db.session.get(Manual, manual_id)
        if not manual:
            raise NotFoundError("Мануал не найден")

        if manual.status != "approved":
            user = db.session.get(User, user_id)
            is_admin = user is not None and user.role == "admin"
            is_author = manual.author_id == user_id

            if not is_admin and not is_author:
                raise ForbiddenError("Мануал не был допущен к публикации")

        return manual

    @staticmethod
    def _get_step_for_user(manual_id: int, step_id: int, user_id: int) -> ManualStep:
        """
        Возвращает шаг мануала с проверкой прав (автор мануала или админ).
        """
        from app.models.user import User

        manual = db.session.get(Manual, manual_id)
        if not manual:
            raise NotFoundError("Мануал не найден")

        user = db.session.get(User, user_id)
        is_admin = user is not None and user.role == "admin"

        if manual.author_id != user_id and not is_admin:
            raise ForbiddenError("Вы можете редактировать только свои мануалы")

        step = None
        for s in manual.steps:
            if s.id == step_id:
                step = s
                break

        if not step:
            raise NotFoundError("Шаг не найден")

        return step

    @staticmethod
    def update_step_image(manual_id: int, step_id: int, user_id: int, file) -> str:
        """
        Сохраняет изображение шага, возвращает путь.
        """
        from app.utils.files import save_step_image

        step = ManualService._get_step_for_user(manual_id, step_id, user_id)

        image_url = save_step_image(file, manual_id, step_id)
        step.image = image_url
        db.session.commit()

        return image_url

    @staticmethod
    def delete_step_image(manual_id: int, step_id: int, user_id: int) -> None:
        """
        Удаляет изображение шага.
        """
        from app.utils.files import delete_file

        step = ManualService._get_step_for_user(manual_id, step_id, user_id)

        if step.image:
            delete_file(step.image)
            step.image = None
            db.session.commit()

    @staticmethod
    def delete_manual(manual_id: int, user_id: int) -> None:
        """Удаляет мануал"""
        manual = db.session.get(Manual, manual_id)
        if not manual:
            raise NotFoundError("Мануал не найден")

        if manual.author_id != user_id:
            raise ForbiddenError("Вы можете удалять только свои мануалы")

        db.session.delete(manual)
        db.session.commit()

    @staticmethod
    def get_manual_for_maintenance_endpoint(
        maintenance_id: int,
        moto_id: int,
        user_id: int,
    ) -> Optional[dict]:
        """
        Полный флоу для эндпоинта GET /api/manual/.

        Проверяет права на обслуживание и мотоцикл, находит подходящий
        мануал, сериализует в формат ответа API.

        Возвращает None, если мануал не найден (API отдаст []).
        """
        from app.models.maintenance import Maintenance
        from app.models.motorcycle import Motorcycle
        from app.models.user import User

        maintenance = db.session.get(Maintenance, maintenance_id)
        motorcycle = db.session.get(Motorcycle, moto_id)
        user = db.session.get(User, user_id)

        if not maintenance:
            raise NotFoundError("Обслуживание не найдено")
        if not motorcycle:
            raise NotFoundError("Мотоцикл не найден")
        if not user:
            raise NotFoundError("Пользователь не найден")

        if int(maintenance.author_id) != int(user.id):
            raise ForbiddenError("Вы можете выполнять только свое обслуживание")
        if int(motorcycle.owner_id) != int(user.id):
            raise ForbiddenError("Вы не являетесь владельцем этого мотоцикла")

        manual = ManualService.get_manual_for_maintenance(
            maintenance_title=maintenance.title,
            motorcycle_name=motorcycle.name,
            user_id=user.id,
        )

        if not manual:
            return None

        return ManualService._serialize_for_maintenance(manual)


    @staticmethod
    def _serialize_for_maintenance(manual: Manual) -> dict:
        """
        Сериализация мануала для эндпоинта GET /api/manual/.

        Формат отличается от Manual.to_dict() (обрезает description,
        не отдаёт author_username, steps без id/manual_id, null -> "").
        """
        return {
            "id": manual.id,
            "title": manual.title,
            "description": manual.description[:200] if manual.description else "",
            "category": manual.category,
            "difficult": manual.difficult,
            "time_estimate": manual.time_estimate,
            "interval": manual.interval,
            "safety_tip": manual.safety_tip,
            "warnings": manual.warnings,
            "conditions": manual.conditions,
            "docs_links": manual.docs_links,
            "specs": manual.specs,
            "aftercare": manual.aftercare,
            "instruments": manual.instruments or "",
            "parts": manual.parts or "",
            "motorcycle": manual.motorcycle,
            "tip": manual.tip or "",
            "steps": [
                {
                    "order": step.order,
                    "title": step.title or "",
                    "text": step.text or "",
                    "tip": step.tip or "",
                    "warning": step.warning or "",
                    "image": step.image or "",
                    "result": step.result or "",
                }
                for step in sorted(manual.steps, key=lambda s: s.order)
            ],
        }