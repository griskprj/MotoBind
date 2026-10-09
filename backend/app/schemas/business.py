from typing import Optional

from pydantic import BaseModel, EmailStr, Field, model_validator

# ============================================================
# БИЗНЕС-АККАУНТ
# ============================================================


class CreateBusinessAccountSchema(BaseModel):
    type: str = Field(..., pattern="^(master|station)$")
    name: str = Field(..., min_length=2, max_length=120)
    description: Optional[str] = None
    city: Optional[str] = Field(None, max_length=64)
    address: Optional[str] = Field(None, max_length=256)
    phone: Optional[str] = Field(None, max_length=20)
    email: Optional[EmailStr] = None
    website: Optional[str] = Field(None, max_length=256)


class UpdateBusinessAccountSchema(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=120)
    description: Optional[str] = None
    city: Optional[str] = Field(None, max_length=64)
    address: Optional[str] = Field(None, max_length=256)
    phone: Optional[str] = Field(None, max_length=20)
    email: Optional[EmailStr] = None
    website: Optional[str] = Field(None, max_length=256)

    def get_updates(self) -> dict:
        return self.model_dump(exclude_unset=True, exclude_none=True)


# ============================================================
# КЛИЕНТ
# ============================================================


class CreateBusinessClientSchema(BaseModel):
    name: str = Field(..., min_length=2, max_length=120)
    phone: Optional[str] = Field(None, max_length=20)
    email: Optional[EmailStr] = None
    note: Optional[str] = None


class UpdateBusinessClientSchema(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=120)
    phone: Optional[str] = Field(None, max_length=20)
    email: Optional[EmailStr] = None
    note: Optional[str] = None

    def get_updates(self) -> dict:
        return self.model_dump(exclude_unset=True, exclude_none=True)


class LinkClientToUserSchema(BaseModel):
    email: EmailStr


# ============================================================
# МОТОЦИКЛ КЛИЕНТА
# ============================================================


class CreateVehicleSchema(BaseModel):
    name: str = Field(..., min_length=2, max_length=120)
    years: Optional[int] = Field(None, ge=1900, le=2100)
    volume: Optional[int] = Field(None, ge=0, le=10000)
    mileage: Optional[int] = Field(None, ge=0)
    vin: Optional[str] = Field(None, max_length=64)
    license_plate: Optional[str] = Field(None, max_length=20)
    color: Optional[str] = Field(None, max_length=16)
    note: Optional[str] = None


class UpdateVehicleSchema(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=120)
    years: Optional[int] = Field(None, ge=1900, le=2100)
    volume: Optional[int] = Field(None, ge=0, le=10000)
    mileage: Optional[int] = Field(None, ge=0)
    vin: Optional[str] = Field(None, max_length=64)
    license_plate: Optional[str] = Field(None, max_length=20)
    color: Optional[str] = Field(None, max_length=16)
    note: Optional[str] = None

    def get_updates(self) -> dict:
        return self.model_dump(exclude_unset=True, exclude_none=True)
