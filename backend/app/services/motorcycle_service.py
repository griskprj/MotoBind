from datetime import datetime, timezone
from typing import List, Optional

from sqlalchemy.orm import selectinload

from app.exceptions import ValidationError
from app.extensions import db
from app.models.motorcycle import Motorcycle
from app.models.reminder import Reminder
from app.utils.files import delete_file, save_moto_photo
from app.utils.helpers import get_motorcycle_or_404


class MotorcycleService:
    """Сервис для работы с мотоциклами"""

    ALLOWED_UPDATE_FIELDS = {
        "name",
        "years",
        "volume",
        "mileage",
        "color",
        "drive_type",
        "license_plate",
        "vin",
        "note",
    }

    @staticmethod
    def create_motorcycle(owner_id: int, **kwargs) -> Motorcycle:
        """Создает мотоцикл."""
        motorcycle = Motorcycle(owner_id=owner_id, **kwargs)
        db.session.add(motorcycle)
        db.session.commit()
        return motorcycle

    @staticmethod
    def update_motorcycle(moto_id: int, user_id: int, **kwargs) -> Motorcycle:
        """Обновляет данные мотоцикла."""
        moto = MotorcycleService.get_motorcycle_by_id(moto_id, user_id)

        updates = {k: v for k, v in kwargs.items() if k in MotorcycleService.ALLOWED_UPDATE_FIELDS and v is not None}

        new_mileage = updates.pop("mileage", None)

        for key, value in updates.items():
            setattr(moto, key, value)

        if new_mileage is not None:
            MotorcycleService.set_mileage(moto, new_mileage)

        db.session.commit()
        return moto

    @staticmethod
    def update_motorcycle_mileage(moto_id: int, user_id: int, mileage: int) -> Motorcycle:
        """Обновляет пробег мотоцикла."""
        moto = MotorcycleService.get_motorcycle_by_id(moto_id, user_id)

        MotorcycleService.set_mileage(moto, mileage)

        db.session.commit()
        return moto

    @staticmethod
    def _on_mileage_change(moto: Motorcycle) -> None:
        """
        Побочные эффекты при изменении пробега:
        - обновляем timestamp
        - удаляем pending-напоминания об обновлении пробега

        Вызывается ТОЛЬКО из set_mileage
        """
        moto.mileage_updated_at = datetime.now(timezone.utc)
        Reminder.query.filter_by(
            motorcycle_id=moto.id,
            type=Reminder.TYPE_MILEAGE_UPDATE,
            status=Reminder.STATUS_PENDING,
        ).delete(synchronize_session=False)

    @staticmethod
    def set_mileage(moto: Motorcycle, new_mileage: int) -> bool:
        """
        Устанавливает новый пробег, если он изменился.

        Инкапсулирует побочные эффекты:
        - обновление mileage_updated_at
        - сброс pending-напоминаний типа mileage_update

        Возвращает True, если пробег был обновлен
        """
        if new_mileage == moto.mileage:
            return False
        moto.mileage = new_mileage
        MotorcycleService._on_mileage_change(moto)
        return True

    @staticmethod
    def update_note(moto_id: int, user_id: int, note_text: Optional[str]) -> Motorcycle:
        """Обновляет заметки мотоцикла."""
        moto = MotorcycleService.get_motorcycle_by_id(moto_id, user_id)

        note_text = note_text or ""
        if len(note_text) > 128:
            raise ValidationError("Длина заметок не более 128 символов")

        moto.note = note_text
        db.session.commit()
        return moto

    @staticmethod
    def delete_motorcycle(moto_id: int, user_id: int) -> None:
        """Удаляет мотоцикл."""
        moto = MotorcycleService.get_motorcycle_by_id(moto_id, user_id)

        if moto.photo_url:
            delete_file(moto.photo_url)

        db.session.delete(moto)
        db.session.commit()

    @staticmethod
    def get_user_motorcycles(user_id: int) -> List[Motorcycle]:
        """Получает все мотоциклы пользователя с предзагрузкой ТО."""
        return Motorcycle.query.options(selectinload(Motorcycle.maintenances)).filter_by(owner_id=user_id).all()

    @staticmethod
    def get_motorcycle_by_id(moto_id: int, user_id: Optional[int] = None) -> Motorcycle:
        """Получает мотоцикл по ID с проверкой прав."""
        return get_motorcycle_or_404(moto_id, user_id)

    @staticmethod
    def update_moto_photo(moto_id: int, user_id: int, file) -> Motorcycle:
        """Обновляет фото мотоцикла"""
        moto = MotorcycleService.get_motorcycle_by_id(moto_id, user_id)

        if moto.photo_url:
            delete_file(moto.photo_url)

        photo_path = save_moto_photo(file, moto_id)
        if not photo_path:
            raise ValidationError("Недопустимый формат файла. Разрешены: jpg, jpeg, png, gif, bmp, webp")

        moto.photo_url = photo_path
        db.session.commit()
        return moto

    @staticmethod
    def delete_moto_photo(moto_id: int, user_id: int) -> Motorcycle:
        """Удаляет фото мотоцикла."""
        moto = MotorcycleService.get_motorcycle_by_id(moto_id, user_id)

        if moto.photo_url:
            delete_file(moto.photo_url)
            moto.photo_url = None
            db.session.commit()

        return moto
