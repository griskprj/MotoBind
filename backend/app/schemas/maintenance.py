from typing import Optional
from pydantic import BaseModel, Field, model_validator

from .mixins import CompletedDateValidatorMixin, DateValidatorMixin

class CreateMaintenanceSchema(DateValidatorMixin, BaseModel):
    motorcycle_id: int = Field(..., alias="motorcycleId")
    category: str = Field(..., min_length=1)
    title: str = Field(..., min_length=1)
    description: Optional[str] = Field(None)
    planned_mileage: Optional[int] = Field(None, ge=0)
    planned_date: Optional[str] = Field(None)
    completed_mileage: Optional[int] = Field(None, ge=0)
    completed_date: Optional[str] = Field(None)
    cost: Optional[int] = Field(None, ge=0)

    @model_validator(mode="after")
    def validate_exclusive_fields(self) -> "CreateMaintenanceSchema":
        """Проверяет, что нельзя указать одновременно planned и completed поля"""
        has_planned = self.planned_mileage is not None or self.planned_date is not None
        has_completed = self.completed_mileage is not None or self.completed_date is not None
        
        if has_planned and has_completed:
            raise ValueError("Нельзя одновременно указывать плановые и выполненные поля")
        
        if has_completed and self.completed_date is None:
            raise ValueError("При указании completed_mileage требуется completed_date")
        
        return self


class UpdateMaintenanceSchema(DateValidatorMixin, BaseModel):
    maintenance_id: int = Field(..., alias="maintenanceId")
    motorcycle_id: Optional[int] = Field(None, alias="motorcycleId")
    category: Optional[str] = Field(None, min_length=1)
    title: Optional[str] = Field(None, min_length=1)
    description: Optional[str] = Field(None)
    planned_mileage: Optional[int] = Field(None, ge=0)
    planned_date: Optional[str] = Field(None)
    completed_mileage: Optional[int] = Field(None, ge=0)
    completed_date: Optional[str] = Field(None)
    cost: Optional[int] = Field(None, ge=0)

    @model_validator(mode="after")
    def validate_completed_fields(self) -> "UpdateMaintenanceSchema":
        if self.completed_mileage is not None and self.completed_date is None:
            raise ValueError("При указании completed_mileage требуется completed_date")
        return self

    def get_updates(self) -> dict:
        data = self.model_dump(exclude_unset=True)
        data.pop("maintenance_id", None)
        return {k: v for k, v in data.items() if v is not None}


class MarkMaintenanceAsCompletedSchema(CompletedDateValidatorMixin, BaseModel):
    completed_mileage: int = Field(..., ge=0, le=1_000_000)
    completed_date: Optional[str] = Field(None)
    cost: Optional[int] = Field(None, ge=0)
    is_repeat: bool = Field(False)
    interval: Optional[int] = Field(None, ge=0, le=1_000_000)

    @model_validator(mode="after")
    def validate_repeat(self) -> "MarkMaintenanceAsCompletedSchema":
        if self.is_repeat and self.interval is None:
            raise ValueError("При is_repeat=True необходимо указать interval")
        return self