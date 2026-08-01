"""
Базовые тесты для проверки работоспособности API.
Запуск: python -m pytest tests/
"""

import json

import pytest
from app import create_app
from app.extensions import db as _db


@pytest.fixture
def app():
    """Создает тестовое приложение"""
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory"
    return app


@pytest.fixture
def client(app):
    """Создает тестовый клиент"""
    return app.test_client()


@pytest.fixture
def db(app):
    """Создает тестовую БД"""
    with app.app_context():
        _db.create_all()
        yield _db
        _db.drop_all()


def test_register(client, db):
    """Тест регистрации"""
    response = client.post(
        "/api/auth/register",
        json={
            "email": "test@example.com",
            "password": "123456",
            "username": "TestUser",
            "role": "motorcyclist",
        },
    )
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data["message"] == "Регистрация успешна"
    assert "user" in data


def test_login(client, db):
    """Тест логина"""
    client.post(
        "/api/auth/register",
        json={
            "email": "test@example.com",
            "password": "123456",
            "username": "TestUser",
            "role": "motorcyclist",
        },
    )

    response = client.post(
        "/api/auth/login", json={"email": "test@example.com", "password": "123456"}
    )
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "access_token" in data
    assert "refresh_token" in data


def test_login_wrong_password(client, db):
    """Тест логина с неверным паролем"""
    client.post(
        "/api/auth/register",
        json={
            "email": "test@example.com",
            "password": "123456",
            "username": "TestUser",
            "role": "motorcyclist",
        },
    )

    response = client.post(
        "/api/auth/login",
        json={"email": "test@example.com", "password": "wrong_password"},
    )
    assert response.status_code == 403


def test_me_endpoint(client, db):
    """Тест получения профиля"""
    client.post(
        "/api/auth/register",
        json={
            "email": "test@example.com",
            "password": "123456",
            "username": "TestUser",
            "role": "motorcyclist",
        },
    )

    login_response = client.post(
        "/api/auth/login", json={"email": "test@example.com", "password": "123456"}
    )
    token = json.loads(login_response.data)["access_token"]

    response = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["email"] == "test@example.com"
    assert data["username"] == "TestUser"
