from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime, date


class CreateMaintenanceSchema(BaseModel):
    id: int = Field(..., alias='moto_id')
    category: str = Field(..., min_length=1)
    title: str = Field(..., min_length=1)
    description: Optional[str] = None
    mileage: Optional[int] = Field(None, ge=0)
    cost: Optional[int] = Field(None, ge=0)
    date: Optional[date] = None

    @field_validator('date', mode='before')
    def parse_date(cls, v):
        if isinstance(cls, v):
            return datetime.strptime(v, '%Y-%m-%d').date()
        return v