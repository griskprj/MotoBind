import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Класс для настроек"""

    DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    # База данных
    DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # JWT
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'your-secret-key')
    JWT_ACCESS_TOKEN_EXPIRES = 3600
    JWT_REFRESH_TOKEN_EXPIRES = 2592000
    
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.yandex.ru')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
    MAIL_USE_SSL = os.environ.get('MAIL_USE_SSL', 'False').lower() == 'true'
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'True').lower() == 'true'
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER', 'motobind@yandex.ru')
    FRONTEND_URL = os.environ.get('FRONTEND_URL', 'http://localhost:5173')

    # Robokassa. Payment mode deliberately defaults to test mode.
    ROBOKASSA_MERCHANT_LOGIN = os.environ.get('ROBOKASSA_MERCHANT_LOGIN', '')
    ROBOKASSA_PASSWORD_1 = os.environ.get('ROBOKASSA_PASSWORD_1', '')
    ROBOKASSA_PASSWORD_2 = os.environ.get('ROBOKASSA_PASSWORD_2', '')
    ROBOKASSA_TEST_PASSWORD_1 = os.environ.get('ROBOKASSA_TEST_PASSWORD_1', '')
    ROBOKASSA_TEST_PASSWORD_2 = os.environ.get('ROBOKASSA_TEST_PASSWORD_2', '')
    ROBOKASSA_HASH_ALGORITHM = os.environ.get('ROBOKASSA_HASH_ALGORITHM', 'MD5').upper()
    ROBOKASSA_TEST_MODE = os.environ.get('ROBOKASSA_TEST_MODE', 'true').lower() == 'true'
    ROBOKASSA_PAYMENT_OBJECT = os.environ.get('ROBOKASSA_PAYMENT_OBJECT', 'service')
    ROBOKASSA_TAX = os.environ.get('ROBOKASSA_TAX', 'none')
    ROBOKASSA_PAYMENT_METHOD = os.environ.get('ROBOKASSA_PAYMENT_METHOD', 'full_payment')

    WEBPUSH_VAPID_PUBLIC_KEY = os.environ.get('WEBPUSH_VAPID_PUBLIC_KEY', '')
    WEBPUSH_VAPID_PRIVATE_KEY = os.environ.get('WEBPUSH_VAPID_PRIVATE_KEY', '')
    WEBPUSH_VAPID_SUBJECT = os.environ.get('WEBPUSH_VAPID_SUBJECT', 'mailto:motobind@yandex.ru')

    # Cron
    CRON_SECRET = os.getenv("CRON_SECRET", "")
    ENABLE_DEV_SCHEDULER = os.getenv("ENABLE_DEV_SCHEDULER", "true").lower() == "true"
    DISABLE_SCHEDULER = os.getenv("DISABLE_SCHEDULER", "false").lower() == "true"
    
    # Другие настройки
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key')
    UPLOAD_FOLDER = 'uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB

    @staticmethod
    def get_cors_origins():
        """Возвращает разрешенные CORS-источники"""
        origins = os.environ.get('CORS_ORIGINS', 'http://localhost:5173')
        return [origin.strip() for origin in origins.split(',')]


class TestingConfig(Config):
    """Конфиг для тестов."""
    DEBUG = False
    TESTING = True

    DATABASE_URL = "sqlite://"

    DISABLE_SCHEDULER = True
    ENABLE_DEV_SCHEDULER = False

    MAIL_SUPPRESS_SEND = True
    MAIL_SERVER = "localhost"
    MAIL_USERNAME = "test@test.local"
    MAIL_PASSWORD = "test"
    MAIL_DEFAULT_SENDER = "test@test.local"

    SECRET_KEY = "test-secret-key-not-for-production"
    JWT_SECRET_KEY = "test-jwt-secret-key-not-for-production"

    CORS_ORIGINS = "http://localhost:5173"

settings = Config()
testing_settings = TestingConfig()
