from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class UpdateProfileSchema(BaseModel):
    username: Optional[str] = Field(None, min_length=2, max_length=32)
    email: Optional[EmailStr] = None
    bio: Optional[str] = Field(None, max_length=128)


class ChangePasswordSchema(BaseModel):
    currentPassword: str = Field(..., min_length=1)
    newPassword: str = Field(..., min_length=6, max_length=128)


class DeleteAccountSchema(BaseModel):
    password: str = Field(..., min_length=1)
