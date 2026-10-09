from typing import Optional

from pydantic import BaseModel, Field


class CreateServiceSchema(BaseModel):
    title: str = Field(..., min_length=2, max_length=120)
    description: Optional[str] = None
    category: str = Field(
        ...,
        pattern="^(maintenance|repair|diagnostics|tuning|other)$",
    )
    price_from: Optional[int] = Field(None, ge=0)
    price_to: Optional[int] = Field(None, ge=0)
    duration_min: Optional[int] = Field(None, ge=0, le=100000)


class UpdateServiceSchema(BaseModel):
    title: Optional[str] = Field(None, min_length=2, max_length=120)
    description: Optional[str] = None
    category: Optional[str] = Field(
        None,
        pattern="^(maintenance|repair|diagnostics|tuning|other)$",
    )
    price_from: Optional[int] = Field(None, ge=0)
    price_to: Optional[int] = Field(None, ge=0)
    duration_min: Optional[int] = Field(None, ge=0, le=100000)

    def get_updates(self) -> dict:
        return self.model_dump(exclude_unset=True, exclude_none=True)


class RejectServiceSchema(BaseModel):
    reason: str = Field(..., min_length=3, max_length=256)
