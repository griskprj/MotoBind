from datetime import datetime, timezone
from typing import List, Optional

from app.exceptions import ConflictError, ValidationError
from app.extensions import db
from app.models.maintenance import Maintenance, MaintenanceStatus
from app.models.maintenance_event import MaintenanceEvent, MaintenanceWork, WorkKind
from app.models.motorcycle import Motorcycle
from app.models.reminder import Reminder
from app.utils.files import delete_file, save_moto_photo
from app.utils.helpers import get_motorcycle_or_404
from sqlalchemy.orm import selectinload


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
        confirm_maintenance_deletion = kwargs.pop(
            "confirm_maintenance_deletion", False
        )

        updates = {
            k: v
            for k, v in kwargs.items()
            if k in MotorcycleService.ALLOWED_UPDATE_FIELDS and v is not None
        }

        new_mileage = updates.pop("mileage", None)

        for key, value in updates.items():
            setattr(moto, key, value)

        if new_mileage is not None:
            MotorcycleService._apply_mileage_update(
                moto, new_mileage, confirm_maintenance_deletion
            )

        db.session.commit()
        return moto

    @staticmethod
    def update_motorcycle_mileage(
        moto_id: int,
        user_id: int,
        mileage: int,
        confirm_maintenance_deletion: bool = False,
    ) -> Motorcycle:
        """Обновляет пробег мотоцикла."""
        moto = MotorcycleService.get_motorcycle_by_id(moto_id, user_id)

        MotorcycleService._apply_mileage_update(
            moto, mileage, confirm_maintenance_deletion
        )

        db.session.commit()
        return moto

    @staticmethod
    def _apply_mileage_update(
        moto: Motorcycle, new_mileage: int, confirm_maintenance_deletion: bool
    ) -> int:
        """Удаляет завершённую историю выше откатываемого пробега после подтверждения."""
        should_check_history = (
            new_mileage < (moto.mileage or 0) or confirm_maintenance_deletion
        )
        if not should_check_history:
            MotorcycleService.set_mileage(moto, new_mileage)
            return 0

        legacy_records = Maintenance.query.filter(
            Maintenance.moto_id == moto.id,
            Maintenance.status == MaintenanceStatus.COMPLETED.value,
            Maintenance.completed_mileage > new_mileage,
        ).all()
        events = MaintenanceEvent.query.filter(
            MaintenanceEvent.motorcycle_id == moto.id,
            MaintenanceEvent.mileage.isnot(None),
            MaintenanceEvent.mileage > new_mileage,
        ).all()
        records_to_delete = len(legacy_records) + len(events)

        if records_to_delete and not confirm_maintenance_deletion:
            raise ConflictError(
                f"При уменьшении пробега до {new_mileage} км будут удалены "
                f"все выполненные ТО с пробегом выше этого значения ({records_to_delete})."
            )

        affected_component_ids = set()
        if events:
            event_ids = [event.id for event in events]
            affected_component_ids = {
                component_id
                for (component_id,) in db.session.query(MaintenanceWork.component_id)
                .filter(
                    MaintenanceWork.event_id.in_(event_ids),
                    MaintenanceWork.kind == WorkKind.REPLACE,
                    MaintenanceWork.component_id.isnot(None),
                )
                .all()
            }

        for record in legacy_records:
            db.session.delete(record)
        for event in events:
            db.session.delete(event)
        db.session.flush()

        if affected_component_ids:
            from app.services.event_service import EventService

            EventService._recalc_components_by_ids(affected_component_ids)

        MotorcycleService.set_mileage(moto, new_mileage)
        return records_to_delete

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
        return (
            Motorcycle.query.options(selectinload(Motorcycle.maintenances))
            .filter_by(owner_id=user_id)
            .all()
        )

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
            raise ValidationError(
                "Недопустимый формат файла. Разрешены: jpg, jpeg, png, gif, bmp, webp"
            )

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
