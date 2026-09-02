from typing import Optional, Dict

from pydantic import BaseModel, EmailStr, Field


class UpdateProfileSchema(BaseModel):
    username: Optional[str] = Field(None, min_length=2, max_length=32)
    email: Optional[EmailStr] = None
    bio: Optional[str] = Field(None, max_length=128)
    location: Optional[str] = Field(None, max_length=128)
    motorcycle: Optional[str] = Field(None, max_length=128)
    experience: Optional[str] = Field(None, pattern="^(beginner|intermediate|expert)$")
    social_links: Optional[Dict[str, str]] = None

    def get_updates(self) -> dict:
        return {k: v for k, v in self.model_dump().items() if v is not None}


class ChangePasswordSchema(BaseModel):
    currentPassword: str = Field(..., min_length=1)
    newPassword: str = Field(..., min_length=6, max_length=128)


class DeleteAccountSchema(BaseModel):
    password: str = Field(..., min_length=1)
