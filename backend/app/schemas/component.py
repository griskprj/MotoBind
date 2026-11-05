from datetime import date, datetime
from typing import Literal, Optional

from app.schemas.mixins import ISO8601Mixin
from pydantic import BaseModel, ConfigDict, Field

ComponentCategoryLiteral = Literal[
    "fluid", "filter", "ignition", "brake", "drive", "other"
]
ConditionRatingLiteral = Literal["good", "ok", "bad", "unknown"]


# ---------- Request ----------


class CreateComponentSchema(BaseModel):
    name: str = Field(..., min_length=1, max_length=80)
    category: ComponentCategoryLiteral = "other"
    manufacturer: Optional[str] = Field(None, max_length=80)
    part_number: Optional[str] = Field(None, max_length=80)
    interval_km: Optional[int] = Field(None, ge=0)
    interval_days: Optional[int] = Field(None, ge=0)
    last_service_date: Optional[str] = Field(None)
    last_service_mileage: Optional[int] = Field(None, ge=0)
    condition_rating: Optional[ConditionRatingLiteral] = None
    condition_note: Optional[str] = Field(None, max_length=256)

    model_config = {"str_strip_whitespace": True}


class UpdateComponentSchema(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=80)
    category: Optional[ComponentCategoryLiteral] = None
    manufacturer: Optional[str] = Field(None, max_length=80)
    part_number: Optional[str] = Field(None, max_length=80)
    interval_km: Optional[int] = Field(None, ge=0)
    interval_days: Optional[int] = Field(None, ge=0)
    last_service_date: Optional[str] = Field(None)
    last_service_mileage: Optional[int] = Field(None, ge=0)
    condition_rating: Optional[ConditionRatingLiteral] = None
    condition_note: Optional[str] = Field(None, max_length=256)

    model_config = {"str_strip_whitespace": True}

    def get_updates(self) -> dict:
        """Только переданные поля. Удаление значения — явным null (см. exclude_unset)."""
        return self.model_dump(exclude_unset=True)


class ApplyTemplateSchema(BaseModel):
    style: Literal["calm", "normal", "aggressive"] = "normal"
    terrain: Literal["city", "highway", "mixed", "dusty", "offroad"] = "mixed"


# ---------- Response ----------


class ComponentResponseSchema(ISO8601Mixin, BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    motorcycle_id: int
    template_key: Optional[str] = None
    name: str
    category: str
    manufacturer: Optional[str] = None
    part_number: Optional[str] = None
    interval_km: Optional[int] = None
    interval_days: Optional[int] = None
    last_service_date: Optional[date] = None
    last_service_mileage: Optional[int] = None
    condition_rating: Optional[str] = None
    condition_note: Optional[str] = None
    is_active: bool
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class ComponentListResponseSchema(BaseModel):
    components: list[ComponentResponseSchema]
    total: int


class ApplyTemplateResponseSchema(BaseModel):
    created: list[dict]
    skipped: list[dict]
    drive_type: str
    counts: dict


# ---------- История ----------


class ComponentHistoryEventSchema(BaseModel):
    """Событие, к которому относится работа."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    date: date
    mileage: Optional[int] = None
    comment: Optional[str] = None


class ComponentHistoryItemSchema(ISO8601Mixin, BaseModel):
    """Одна работа по компоненту."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    event_id: int
    component_id: Optional[int] = None
    kind: str
    title: Optional[str] = None
    cost: int = 0
    note: Optional[str] = None
    created_at: Optional[datetime] = None
    event: Optional[ComponentHistoryEventSchema] = None


class ComponentHistoryResponseSchema(BaseModel):
    component: ComponentResponseSchema
    history: list[ComponentHistoryItemSchema]
