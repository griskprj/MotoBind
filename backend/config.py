import os

from pydantic import Field, field_validator, validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Базовые настройки приложения с валидацией через pydantic"""

    SECRET_KEY: str = Field(..., min_length=32, description="Секретный ключ Flask")
    DEBUG: bool = False
    ENV: str = "development"  # development, production, testing

    DATABASE_URL: str = Field(..., description="URL подключение к БД")
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False

    JWT_SECRET_KEY: str = Field(..., min_length=32, description="Секрет для JWT")
    JWT_ACCESS_TOKEN_EXPIRES: int = 3600  # 60 мин
    JWT_REFRESH_TOKEN_EXPIRES: int = 2592000  # 30 дн
    JWT_REFRESH_TOKEN_COOKIE_NAME: str = "refresh_token"
    JWT_COOKIE_SECURE: bool = False
    JWT_COOKIE_CSRF_PROTECT: bool = True
    JWT_TOKEN_LOCATION: list = ["headers", "cookies"]

    UPLOAD_FOLDER: str = "uploads"
    MAX_CONTENT_LENGTH: int = 50 * 1024 * 1024  # 50 MB
    BASE_URL: str = "http://localhost:5000"

    CORS_ORIGINS: str = "*"

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=True, extra="ignore"
    )

    @field_validator("DATABASE_URL")
    def validate_database_url(cls, v):
        if not v.startswith(("postgresql://", "sqlite://", "mysql://")):
            raise ValueError(
                "DATABASE_URL должен начинаться с postgresql://, sqlite:// или mysql://"
            )
        return v

    @field_validator("SECRET_KEY", "JWT_SECRET_KEY")
    def validate_secret_keys(cls, v):
        if len(v) < 32:
            raise ValueError("Длина секретного ключа должна быть не меньше 32 символов")
        return v

    def get_cors_origins(self):
        """Возвращает список разрешенных CORS-источников"""
        if self.CORS_ORIGINS == "*":
            return ["*"]
        return [
            origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()
        ]


def get_settings() -> Settings:
    """Возвращает экземпляр настроек с учетом переменной ENV"""
    env = os.getenv("ENV", "development")
    settings = Settings()

    if env == "testing":
        if not os.getenv("DATABASE_URL"):
            settings.DATABASE_URL = "sqlite:///test.db"
        settings.DEBUG = False
    return settings


settings = get_settings()
