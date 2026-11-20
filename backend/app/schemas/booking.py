from typing import Optional

from pydantic import BaseModel, Field

# ============================================================
# СОЗДАНИЕ (клиент)
# ============================================================


class CreateBookingSchema(BaseModel):
    business_account_id: int
    service_id: Optional[int] = None
    motorcycle_id: Optional[int] = None
    scheduled_at: str = Field(..., description="ISO 8601 datetime")
    client_note: Optional[str] = Field(None, max_length=1000)


# ============================================================
# ДЕЙСТВИЯ МАСТЕРА
# ============================================================


class DeclineBookingSchema(BaseModel):
    reason: Optional[str] = Field(None, max_length=256)


class RescheduleBookingSchema(BaseModel):
    scheduled_at: str = Field(..., description="ISO 8601 datetime")


class CompleteBookingSchema(BaseModel):
    price_final: Optional[int] = Field(None, ge=0)
    master_note: Optional[str] = None


# ============================================================
# ОТМЕНА (клиент)
# ============================================================


class CancelBookingSchema(BaseModel):
    reason: Optional[str] = Field(None, max_length=256)
