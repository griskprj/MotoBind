"""
Общие pytest fixtures для тестов MotoBind.

Использует in-memory SQLite с StaticPool — одно хранилище
на все соединения, чтобы Flask-SQLAlchemy и test_client
работали с одной и той же БД.
"""

import pytest
from sqlalchemy.pool import StaticPool

from app import create_app
from app.extensions import db as _db
from app.models.user import User


def pytest_configure(config):
    """
    Регистрирует кастомные маркеры.
    """
    for marker, description in [
        ("auth", "tests for auth endpoints"),
        ("motorcycle", "tests for motorcycle endpoints"),
        ("maintenance", "tests for maintenance endpoints"),
        ("statistic", "tests for statistic endpoints"),
        ("slow", "slow tests (skipped by default unless explicitly requested)"),
        ("social", "tests for social endpoints"),
        ("manuals", "tests for manuals endpoints"),
    ]:
        config.addinivalue_line("markers", f"{marker}: {description}")


@pytest.fixture(scope="session")
def app():
    """
    Создаёт тестовое Flask-приложение один раз на всю сессию тестов.

    Важные override:
    - TESTING=True → отключает scheduler, включает propagate exceptions
    - SQLALCHEMY_DATABASE_URI="sqlite://" + StaticPool → одна in-memory БД
    - MAIL_SUPPRESS_SEND=True → письма не уходят
    - DISABLE_SCHEDULER=True → фоновой поток не стартует
    """
    app = create_app(
        config_override={
            "TESTING": True,
            "DEBUG": False,
            "SQLALCHEMY_DATABASE_URI": "sqlite://",
            "SQLALCHEMY_ENGINE_OPTIONS": {
                "connect_args": {"check_same_thread": False},
                "poolclass": StaticPool,
            },
            "SQLALCHEMY_TRACK_MODIFICATIONS": False,
            "DISABLE_SCHEDULER": True,
            "ENABLE_DEV_SCHEDULER": False,
            "MAIL_SUPPRESS_SEND": True,
            "MAIL_SERVER": "localhost",
            "MAIL_USERNAME": "test@test.local",
            "MAIL_PASSWORD": "test",
            "MAIL_DEFAULT_SENDER": "test@test.local",
            "SECRET_KEY": "test-secret-key-not-for-production-0123456789",
            "JWT_SECRET_KEY": "test-jwt-secret-key-not-for-production-0123456789",
        }
    )
    return app


@pytest.fixture(scope="function")
def db_session(app):
    """
    Создаёт схему БД перед тестом и дропает после.
    Каждый тест — чистая БД.
    """
    with app.app_context():
        _db.create_all()
        yield _db
        _db.session.remove()
        _db.drop_all()


@pytest.fixture(scope="function")
def client(app, db_session):
    """
    Flask test client.
    Зависит от db_session, чтобы схема была готова до запросов.
    """
    return app.test_client()


# ---- Email mocks ----


@pytest.fixture(autouse=True)
def mock_email(monkeypatch):
    """
    Отключает реальную отправку email во всех тестах.
    autouse=True — применяется ко всем тестам без явного запроса.
    """
    monkeypatch.setattr("app.utils.email.send_verification_email", lambda user: None)
    monkeypatch.setattr("app.utils.email.send_reset_email", lambda user: True)


# ---- User factories ----


@pytest.fixture
def make_user(client, db_session):
    """
    Фабрика для создания пользователя.

    Использование:
        make_user(email="a@b.com", password="test123456")
        make_user(email="a@b.com", verified=True)
    """
    counter = {"n": 0}

    def _make(email=None, password="test123456", username=None, role="motorcyclist", verified=False):
        counter["n"] += 1
        email = email or f"user{counter['n']}@example.com"
        username = username or f"User{counter['n']}"

        response = client.post(
            "/api/auth/register",
            json={
                "email": email,
                "password": password,
                "username": username,
                "role": role,
            },
        )
        assert response.status_code == 201, f"make_user: register failed: {response.get_json()}"

        if verified:
            user = User.query.filter_by(email=email).first()
            user.is_verified = True
            db_session.session.commit()

        return {"email": email, "password": password, "username": username, "role": role, "verified": verified}

    return _make


@pytest.fixture
def auth_headers(client, make_user):
    """
    Создаёт подтверждённого пользователя, логинит, возвращает заголовки.

    Использование:
        def test_x(client, auth_headers):
            r = client.get("/api/motorcycle/", headers=auth_headers)
    """
    user = make_user(verified=True)

    response = client.post(
        "/api/auth/login",
        json={
            "email": user["email"],
            "password": user["password"],
            "rememberMe": True,
        },
    )
    assert response.status_code == 200, f"auth_headers: login failed: {response.get_json()}"
    token = response.get_json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
