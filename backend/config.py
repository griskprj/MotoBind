import os
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, validator, field_validator


class Settings(BaseSettings):
    """ Базовые настройки приложения с валидацией через pydantic"""

    # общие
    SECRET_KEY: str = Field(..., min_length=32, description="Секретный ключ Flask")
    DEBUG: bool = False
    ENV: str = "development" # development, production, testing

    # база данных
    DATABASE_URL: str = Field(..., description="URL подключение к БД")
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False

    # JWT
    JWT_SECRET_KEY: str = Field(..., min_length=32, description="Секрет для JWT")
    JWT_ACCESS_TOKEN_EXPIRES: int = 900 # 15 мин
    JWT_REFRESH_TOKEN_EXPIRES: int = 2592000 # 30 дн
    JWT_REFRESH_TOKEN_COOKIE_NAME: str = 'refresh_token'
    JWT_COOKIE_SECURE: bool = False
    JWT_COOKIE_CSRF_PROTECT: bool = True
    JWT_TOKEN_LOCATION: list = ['headers', 'cookies']

    # загрузка файлов
    UPLOAD_FOLDER: str = "uploads"
    MAX_CONTENT_LENGTH: int = 50 * 1024 * 1024 # 50 MB

    # CORS
    CORS_ORIGINS: str = "*"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )

    @field_validator("DATABASE_URL")
    def validate_database_url(cls, v):
        if not v.startswith(("postgresql://", "sqlite://", "mysql://")):
            raise ValueError("DATABASE_URL должен начинаться с postgresql://, sqlite:// или mysql://")
        return v
    
    @field_validator("SECRET_KEY", "JWT_SECRET_KEY")
    def validate_secret_keys(cls, v):
        if len(v) < 32:
            raise ValueError("Длина секретного ключа должна быть не меньше 32 символов")
        return v
    
    def get_cors_origins(self):
        """ Возвращает список разрешенных CORS-источников """
        if self.CORS_ORIGINS == "*":
            return ["*"]
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]
    

def get_settings() -> Settings:
    """ Возвращает экземпляр настроек с учетом переменной ENV """
    env = os.getenv("ENV", "development")
    settings = Settings()

    if env == "testing":
        if not os.getenv("DATABASE_URL"):
            settings.DATABASE_URL = "sqlite:///test.db"
        settings.DEBUG = False
    return settings

settings = get_settings()