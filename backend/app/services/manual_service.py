from typing import Optional, List, Dict, Any
from app.models.manual import Manual, ManualStep
from app.extensions import db
from app.exceptions import ForbiddenError, NotFoundError, BusinessLogicError, ValidationError


class ManualService:
    """ Сервис для работы с мануалами """

    @staticmethod
    def create_manual(
        author_id: int,
        title: str,
        category: str,
        motorcycle: str,
        steps: List[Dict[str, Any]],
        description: Optional[str] = None,
        difficult: str = 'easy',
        instruments: Optional[str] = None,
        parts: Optional[str] = None
    ) -> Manual:
        """ Создает мануал с шагами """

        manual = Manual(
            author_id=author_id,
            title=title,
            description=description,
            category=category,
            difficult=difficult,
            instruments=instruments,
            status='moderate'
        )

        db.session.add(manual)
        db.session.flush()

        for step_data in steps:
            step = ManualStep(
                manual_id=manual.id,
                order=step_data['order'],
                title=step_data['title'],
                text=step_data.get('text')
            )
            db.session.add(step)

        db.session.commit()
        return manual
    
    @staticmethod
    def update_manual(
        manual_id: int,
        user_id: int,
        **kwargs
    ) -> Manual:
        """ Обновляет мануал """
        manual = Manual.query.get(manual_id)
        if not manual:
            raise NotFoundError("Мануал не найден")
        
        if manual.author_id != user_id:
            raise ForbiddenError("Вы можете редактировать только свои мануалы")
        
        if 'steps' in kwargs:
            steps_data = kwargs.pop('steps')
            ManualService._update_steps(manual.id, steps_data)

        for key, value, in kwargs.items():
            if hasattr(manual, key) and value is not None:
                setattr(manual, key, value)

        db.session.commit()
        return manual
    
    @staticmethod
    def _update_steps(manual_id: int, steps_data: List[Dict[str, Any]]) -> None:
        """ Обновляет шаги мануала """
        ManualStep.query.filter_by(manual_id=manual_id).delete()

        for step_data in steps_data:
            step = ManualStep(
                manual_id=manual_id,
                order=step_data['order'],
                title=step_data['title'],
                text=step_data.get('text')
            )
            db.session.add(step)