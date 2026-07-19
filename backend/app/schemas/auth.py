from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Literal, Optional
from datetime import datetime


class RegisterSchema(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=128)
    username: str = Field(..., min_length=2, max_length=32)
    role: Literal['motorcyclist', 'motoclub']

class LoginSchema(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=1)

class RefreshSchema(BaseModel):
    refresh_token: str = Field(..., min_length=1)
