import re
from datetime import datetime, date
from typing import Optional, List
from pydantic import BaseModel, ConfigDict, Field, field_serializer, field_validator

from app.schemas.mixins import ISO8601Mixin

# --------- Request-схемы ---------

class MotorcycleValidatorMixin:
    """Общие валидаторы для схем мотоцикла"""

    @field_validator("color")
    @classmethod
    def validate_color(cls, v):
        if v and not re.match(r"^#[0-9a-fA-F]{6}$", v):
            raise ValueError("Цвет должен быть в формате HEX (#FFFFFF)")
        return v

    @field_validator("license_plate")
    @classmethod
    def validate_license_plate(cls, v):
        if v and not (8 <= len(v) <= 9):
            raise ValueError("Неверный формат ГОС номера")
        return v

    @field_validator("vin")
    @classmethod
    def validate_vin(cls, v):
        if v and len(v) != 17:
            raise ValueError("VIN должен содержать 17 символов")
        return v


class CreateMotorcycleSchema(MotorcycleValidatorMixin, BaseModel):
    name: str = Field(..., min_length=1, max_length=128)
    years: Optional[int] = Field(None, ge=1900, le=datetime.now().year)
    volume: Optional[int] = Field(None, ge=49, le=4000)
    mileage: Optional[int] = Field(None, ge=0, le=1_000_000)
    color: Optional[str] = None
    license_plate: Optional[str] = Field(None, alias="licensePlate")
    vin: Optional[str] = None
    note: Optional[str] = Field(None, max_length=128)

    model_config = {"populate_by_name": True}


class UpdateMotorcycleSchema(MotorcycleValidatorMixin, BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=128)
    years: Optional[int] = Field(None, ge=1900, le=datetime.now().year)
    volume: Optional[int] = Field(None, ge=49, le=4000)
    mileage: Optional[int] = Field(None, ge=0, le=1_000_000)
    color: Optional[str] = None
    license_plate: Optional[str] = Field(None, alias="licensePlate")
    vin: Optional[str] = None
    note: Optional[str] = Field(None, max_length=128)

    model_config = {"populate_by_name": True}

    def get_updates(self) -> dict:
        """
        Возвращает только переданные поля в snake_case.
        Пустые/None значения отбрасываются, чтобы не перетирать существующие.
        """
        return self.model_dump(exclude_unset=True, exclude_none=True)


# --------- Response-схемы ---------


class MaintenanceShortSchema(ISO8601Mixin, BaseModel):
    """Вложенная схема ТО (совпадает по полям с Maintenance.to_dict())"""

    model_config = ConfigDict(from_attributes=True)

    id: int
    author_id: int
    moto_id: int
    title: str
    description: Optional[str] = None
    category: str
    cost: int = 0
    completed_mileage: Optional[int] = None
    planned_mileage: Optional[int] = None
    completed_date: Optional[date] = None
    planned_date: Optional[date] = None
    status: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class MotorcycleShortSchema(ISO8601Mixin, BaseModel):
    """Ответ без вложенных ТО (используется при создании)"""

    model_config = ConfigDict(from_attributes=True)

    id: int
    owner_id: int
    name: str
    years: Optional[int] = None
    volume: Optional[int] = None
    mileage: Optional[int] = None
    color: Optional[str] = None
    license_plate: Optional[str] = None
    note: Optional[str] = None
    vin: Optional[str] = None
    photo_url: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class MotorcycleDetailSchema(MotorcycleShortSchema):
    """Ответ с вложенными ТО (используется в GET, PUT, PATCH, photo)"""

    maintenances: List[MaintenanceShortSchema] = Field(default_factory=list)