from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime
import re


class CreateMotorcycleSchema(BaseModel):
    name: str = Field(..., min_length=1, max_length=128)
    years: Optional[int] = Field(None, ge=1900, le=datetime.now().year)
    volume: Optional[int] = Field(None, ge=49, le=4000)
    mileage: Optional[int] = Field(None, ge=0, le=1_000_000)
    color: Optional[str] = None
    license_plate: Optional[str] = None
    vin: Optional[str] = None

    @field_validator('color')
    def validate_color(cls, v):
        if v and not re.match(r'^#[0-9a-fA-F]{6}$', v):
            raise ValueError('Цвет должен быть в формате HEX (#FFFFFF)')
        return v
    
    @field_validator('license_plate')
    def validate_license_plate(cls, v):
        if v and not (8 <= len(v) <= 9):
            raise ValueError('Неверный формат ГОС номера')
        return v

    @field_validator('vin')
    def validate_vin(cls, v):
        if v and len(v) != 17:
            raise ValueError('VIN должен содержать 17 символов')
        return v
    
class  UpdateMotorcycleSchema(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=128)
    years: Optional[int] = Field(None, ge=1900, le=datetime.now().year)
    volume: Optional[int] = Field(None, ge=49, le=4000)
    mileage: Optional[int] = Field(None, ge=0, le=1_000_000)
    color: Optional[str] = None
    license_plate: Optional[str] = None
    vin: Optional[str] = None

    @field_validator('color')
    def validate_color(cls, v):
        if v and not re.match(r'^#[0-9a-fA-F]{6}$', v):
            raise ValueError('Цвет должен быть в формате HEX (#FFFFFF)')
        return v

    @field_validator('license_plate')
    def validate_license_plate(cls, v):
        if v and not (8 <= len(v) <= 9):
            raise ValueError('Неверный формат ГОС номера')
        return v

    @field_validator('vin')
    def validate_vin(cls, v):
        if v and len(v) != 17:
            raise ValueError('VIN должен содержать 17 символов')
        return v
    
    def get_updates(self) -> dict:
        """ Возвращает только те поля, которые были переданы """
        raise {k: v for k, v in self.model_dump().items() if v is not None}
    