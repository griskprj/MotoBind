from datetime import date, datetime
from typing import Any, Optional

from pydantic import BaseModel, field_serializer, field_validator


class DateValidatorMixin:
    @field_validator("planned_date", "completed_date", mode="before", check_fields=False)
    @classmethod
    def validate_date(cls, v: Any) -> Optional[str]:
        if v is None or v == "":
            return None
        if isinstance(v, str):
            try:
                datetime.strptime(v, "%Y-%m-%d")
                return v
            except ValueError:
                raise ValueError("Неверный формат даты. Используйте ГГГГ-ММ-ДД")
        raise ValueError(f"Неподдерживаемый тип для даты: {type(v)}")


class PlannedDateValidatorMixin:
    @field_validator("planned_date", mode="before", check_fields=False)
    @classmethod
    def validate_planned_date(cls, v: Any) -> Optional[str]:
        if v is None or v == "":
            return None
        if isinstance(v, str):
            try:
                datetime.strptime(v, "%Y-%m-%d")
                return v
            except ValueError:
                raise ValueError("Неверный формат даты. Используйте ГГГГ-ММ-ДД")
        raise ValueError(f"Неподдерживаемый тип для даты: {type(v)}")


class CompletedDateValidatorMixin:
    @field_validator("completed_date", mode="before", check_fields=False)
    @classmethod
    def validate_completed_date(cls, v: Any) -> Optional[str]:
        if v is None or v == "":
            return None
        if isinstance(v, str):
            try:
                datetime.strptime(v, "%Y-%m-%d")
                return v
            except ValueError:
                raise ValueError("Неверный формат даты. Используйте ГГГГ-ММ-ДД")
        raise ValueError(f"Неподдерживаемый тип для даты: {type(v)}")


class ISO8601Mixin(BaseModel):
    """
    Сериализует datetime/date как .isoformat() - сохраняет формат,
    который отдавал Maintenance.to_dict() до рефакторинга.
    """

    @field_serializer(
        "created_at",
        "updated_at",
        "completed_date",
        "planned_date",
        "last_login",
        check_fields=False,
        when_used="always",
    )
    def _serialize_datetime(self, value, _info):
        if isinstance(value, (datetime, date)):
            return value.isoformat()
        return value
