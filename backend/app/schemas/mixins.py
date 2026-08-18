from datetime import datetime
from typing import Any, Optional
from pydantic import field_validator

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