from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.schemas.mixins import ISO8601Mixin


class RegisterSchema(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=128)
    username: str = Field(..., min_length=2, max_length=32)
    role: Literal["motorcyclist", "motoclub"]


class LoginSchema(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=1)
    rememberMe: bool = Field(...)


class RefreshSchema(BaseModel):
    refresh_token: str = Field(..., min_length=1)


# --------- Response-схемы ---------


class UserResponseSchema(ISO8601Mixin, BaseModel):
    """
    Схема пользоавтеля в ответах auth.

    Поля совпадают с User.to_dict() (без include_moto, без include_stats).
    """

    model_config = ConfigDict(from_attributes=True)

    id: int
    email: str
    username: str
    bio: Optional[str] = None
    location: Optional[str] = None
    motorcycle: Optional[str] = None
    experience: Optional[str] = None
    social_links: Optional[dict] = None
    avatar: Optional[str] = None
    role: str
    status: Optional[str] = None
    created_at: Optional[datetime] = None
    last_login: Optional[datetime] = None
    email_notifications_enabled: bool = True
    email_newsletter_enabled: bool = True
    email_verification_enabled: bool = True
    reminders_mileage_enabled: bool = True
    reminders_maintenance_enabled: bool = True


class LoginResponseSchema(BaseModel):
    """Ответ POST /api/auth/login."""

    message: str
    access_token: str
    refresh_token: Optional[str] = None
    user: UserResponseSchema


class RegisterResponseSchema(BaseModel):
    """Ответ POST /api/auth/register."""

    message: str
    access_token: str
    refresh_token: str
    user: UserResponseSchema
    requires_verification: bool = True


class RefreshResponseSchema(BaseModel):
    """Ответ POST /api/auth/refresh."""

    access_token: str
    refresh_token: str


class VerifyEmailResponseSchema(BaseModel):
    """Ответ GET /api/auth/verify-email/<token>."""

    message: str
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None
    user: Optional[UserResponseSchema] = None


class MessageResponseSchema(BaseModel):
    """Универсальный ответ с message (logout, send-verification, forgot-password, reset-password)."""

    message: str


class CheckVerificationResponseSchema(BaseModel):
    """Ответ GET /api/auth/check-verification."""

    is_verified: bool


class CheckResetTokenResponseSchema(BaseModel):
    """Ответ GET /api/auth/check-reset-token/<token>."""

    valid: bool
    email: Optional[str] = None
