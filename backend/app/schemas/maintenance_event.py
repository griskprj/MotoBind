from datetime import date, datetime
from typing import Literal, Optional

from app.schemas.mixins import ISO8601Mixin
from pydantic import BaseModel, ConfigDict, Field, model_validator

WorkKindLiteral = Literal["replace", "inspect", "adjust", "repair", "other"]


# ---------- Request ----------


class CreateWorkSchema(BaseModel):
    component_id: Optional[int] = Field(None, ge=1)
    kind: WorkKindLiteral = "other"
    title: Optional[str] = Field(None, max_length=80)
    cost: Optional[int] = Field(None, ge=0)
    note: Optional[str] = None

    model_config = {"str_strip_whitespace": True}

    @model_validator(mode="after")
    def _require_title_or_component(self):
        if self.component_id is None and not (self.title and self.title.strip()):
            raise ValueError("Укажите component_id или title")
        return self


class CreateEventSchema(BaseModel):
    motorcycle_id: int = Field(..., alias="motorcycleId")
    date: str = Field(..., description="YYYY-MM-DD")
    mileage: Optional[int] = Field(None, ge=0, le=1_000_000)
    total_cost: Optional[int] = Field(None, ge=0, alias="totalCost")
    comment: Optional[str] = None
    works: list[CreateWorkSchema] = Field(..., min_length=1)

    model_config = {"populate_by_name": True, "str_strip_whitespace": True}


class UpdateEventSchema(BaseModel):
    date: Optional[str] = None
    mileage: Optional[int] = Field(None, ge=0, le=1_000_000)
    total_cost: Optional[int] = Field(None, ge=0, alias="totalCost")
    comment: Optional[str] = None
    works: Optional[list[CreateWorkSchema]] = None

    model_config = {"populate_by_name": True, "str_strip_whitespace": True}

    def get_updates(self) -> dict:
        return self.model_dump(exclude_unset=True)


# ---------- Response ----------


class WorkResponseSchema(ISO8601Mixin, BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    event_id: int
    component_id: Optional[int] = None
    kind: str
    title: Optional[str] = None
    cost: int = 0
    note: Optional[str] = None
    created_at: Optional[datetime] = None


class EventResponseSchema(ISO8601Mixin, BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    motorcycle_id: int
    date: date
    mileage: Optional[int] = None
    total_cost: int = 0
    comment: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    works: list[WorkResponseSchema] = []


class EventListResponseSchema(BaseModel):
    events: list[EventResponseSchema]
    total: int
    page: int
    per_page: int
    pages: int
