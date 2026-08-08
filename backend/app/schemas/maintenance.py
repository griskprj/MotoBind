from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, Field, field_validator


class CreateMaintenanceSchema(BaseModel):
    """Схема для создания записи ТО"""
    motorcycle_id: int = Field(..., alias="motorcycleId", description="ID мотоцикла")
    category: str = Field(..., min_length=1, description="Категория ТО")
    title: str = Field(..., min_length=1, description="Название ТО")
    description: Optional[str] = Field(None, description="Описание")
    mileage: Optional[int] = Field(None, ge=0, description="Пробег на момент ТО")
    cost: Optional[int] = Field(None, ge=0, description="Стоимость")
    date: Optional[str] = Field(None, description="Дата проведения (ГГГГ-ММ-ДД)")

    @field_validator("date", mode="before")
    @classmethod
    def validate_date(cls, v: Any) -> Optional[str]:
        """Проверяет, что дата соответствует формату ГГГГ-ММ-ДД или равна None."""
        if v is None or v == "":
            return None
        if isinstance(v, str):
            try:
                datetime.strptime(v, "%Y-%m-%d")
                return v
            except ValueError:
                raise ValueError("Неверный формат даты. Используйте ГГГГ-ММ-ДД")
        # Если пришёл не строковый тип, можно попробовать конвертировать
        raise ValueError(f"Неподдерживаемый тип для даты: {type(v)}. Ожидается строка в формате ГГГГ-ММ-ДД")


class CreatePlannedMaintenanceSchema(BaseModel):
    """Схема для создания планового ТО"""
    motorcycle_id: int = Field(..., alias="motorcycleId", description="ID мотоцикла")
    category: str = Field(..., min_length=1, description="Категория ТО")
    title: str = Field(..., min_length=1, description="Название ТО")
    description: Optional[str] = Field(None, description="Описание")
    planned_mileage: int = Field(..., ge=0, description="Плановый пробег")


class UpdatePlannedMaintenanceSchema(BaseModel):
    """Схема для обновления планового ТО"""
    maintenance_id: int = Field(..., alias="maintenanceId", description="ID записи планового ТО")
    motorcycle_id: Optional[int] = Field(None, alias="motorcycleId", description="ID мотоцикла")
    category: Optional[str] = Field(None, min_length=1, description="Категория ТО")
    title: Optional[str] = Field(None, min_length=1, description="Название ТО")
    description: Optional[str] = Field(None, description="Описание")
    planned_mileage: Optional[int] = Field(None, alias="mileage", ge=0, description="Плановый пробег")

    def get_updates(self) -> dict:
        """Возвращает только переданные поля (исключая maintenance_id)"""
        return {
            k: v
            for k, v in self.model_dump(exclude_unset=True, exclude_none=True).items()
            if k != "maintenance_id" and v is not None
        }


class MarkPlannedMaintenanceSchema(BaseModel):
    """Схема для отметки планового ТО как выполненного"""
    maintenance_id: int = Field(..., alias="id", description="ID планового ТО")
    mileage: int = Field(..., ge=0, le=1_000_000, description="Пробег при выполнении")
    date: Optional[str] = Field(None, description="Дата выполнения (ГГГГ-ММ-ДД)")
    cost: Optional[int] = Field(None, ge=0, description="Стоимость")
    is_repeat: Optional[bool] = Field(False, description="Повторять ТО?")
    interval: Optional[int] = Field(None, ge=0, le=1_000_000, description="Интервал повторения")

    @field_validator("date", mode="before")
    @classmethod
    def validate_date(cls, v: Any) -> Optional[str]:
        """Проверяет, что дата соответствует формату ГГГГ-ММ-ДД или равна None."""
        if v is None or v == "":
            return None
        if isinstance(v, str):
            try:
                datetime.strptime(v, "%Y-%m-%d")
                return v
            except ValueError:
                raise ValueError("Неверный формат даты. Используйте ГГГГ-ММ-ДД")
        raise ValueError(f"Неподдерживаемый тип для даты: {type(v)}. Ожидается строка в формате ГГГГ-ММ-ДД")