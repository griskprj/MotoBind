from typing import Literal, Optional

from pydantic import BaseModel, EmailStr, Field


class CreateUserSchema(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=2, max_length=32)
    password: str = Field(..., min_length=6, max_length=128)
    role: Literal["motorcyclist", "motoclub", "admin"] = "motorcyclist"
    status: Literal["active", "banned"] = "active"


class UpdateUserSchema(BaseModel):
    username: Optional[str] = Field(None, min_length=2, max_length=32)
    email: Optional[EmailStr] = None
    role: Optional[Literal["motorcyclist", "motoclub", "admin"]] = None
    status: Optional[Literal["active", "banned"]] = None

    def get_updates(self) -> dict:
        return {k: v for k, v in self.model_dump().items() if v is not None}
