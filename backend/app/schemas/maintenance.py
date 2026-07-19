from pydantic import BaseModel, Field, field_validator
from typing import Optional, Any
from datetime import datetime, date


class CreateMaintenanceSchema(BaseModel):
    id: int = Field(..., alias='id')
    category: str = Field(..., min_length=1)
    title: str = Field(..., min_length=1)
    description: Optional[str] = None
    mileage: Optional[int] = Field(None, ge=0)
    cost: Optional[int] = Field(None, ge=0)
    date: Any = None

    @field_validator('date', mode='before')
    @classmethod
    def parse_date(cls, v: Any) -> Optional[date]:
        """Преобразует любой ввод в объект date или None."""
        if v is None:
            return None
        if isinstance(v, date):
            return v
        if isinstance(v, str):
            try:
                return datetime.strptime(v, '%Y-%m-%d').date()
            except ValueError:
                raise ValueError('Неверный формат даты. Используйте ГГГГ-ММ-ДД')
        if isinstance(v, datetime):
            return v.date()
        raise ValueError(f'Неподдерживаемый тип для даты: {type(v)}')
    
class CreatePlannedMaintenanceSchema(BaseModel):
    id: int = Field(..., alias='id')
    category: str = Field(..., min_length=1)
    title: str = Field(..., min_length=1)
    description: Optional[str] = None
    planned_mileage: int = Field(..., ge=0)

class UpdatePlannedMaintenanceShema(BaseModel):
    maintenance_id: int = Field(..., alias='maintenanceId')
    moto_id: Optional[int] = Field(None, alias='motorcycleId')
    category: Optional[str] = Field(None, min_length=1)
    title: Optional[str] = Field(None, min_length=1)
    description: Optional[str] = None
    planned_mileage: Optional[int] = Field(None, alias='mileage', ge=0)

    def get_updates(self) -> dict:
        """Возвращает только переданные поля (исключая maintenance_id)"""
        return {
            k: v for k, v in self.model_dump(
                exclude_unset=True, 
                exclude_none=True
            ).items() 
            if k != 'maintenance_id' and v is not None
        }
    
class MarkPlannedMaintenanceSchema(BaseModel):
    planned_id: int = Field(..., alias='id')
    mileage: int = Field(..., ge=0, le=1_000_000)
    date: Any = None
    cost: Optional[int] = Field(None, ge=0)
    is_repeat: Optional[bool] = False
    interval: Optional[int] = Field(None, ge=0, le=1_000_000)

    @field_validator('date', mode='before')
    @classmethod
    def parse_date(cls, v: Any) -> Optional[date]:
        """Преобразует любой ввод в объект date или None."""
        if v is None:
            return None
        if isinstance(v, date):
            return v
        if isinstance(v, str):
            try:
                return datetime.strptime(v, '%Y-%m-%d').date()
            except ValueError:
                raise ValueError('Неверный формат даты. Используйте ГГГГ-ММ-ДД')
        if isinstance(v, datetime):
            return v.date()
        raise ValueError(f'Неподдерживаемый тип для даты: {type(v)}')