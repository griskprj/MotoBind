import pytest
from flask import Flask
from flask_jwt_extended import create_access_token
from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.motorcycle import Motorcycle
from app.models.maintenance import Maintenance, PlannedMaintenance
from app.models.manual import Manual, ManualStep

@pytest.fixture
def app():
    """ Создает тестовое приложение """
    app = create_app()
    app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'JWT_SECRET_KEY': 'test-key-32-chars-long!!!',
        'SECRET_KEY': 'test-secret-key-32-chars-long!!!'
    })

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """ Тестовый клиент """
    return app.test_client()

@pytest.fixture
def db_session(app):
    """ Сессия БД для тестов """
    with app.app_context():
        yield db.session

@pytest.fixture
def test_user(db_session):
    """ Создает тестового пользователя """
    user = User(
        email="test@example.com",
        username="testuser",
        role="motorcyclist",
        status="active"
    )
    user.set_password("password123")
    db_session.add(user)
    db_session.commit()
    return user

@pytest.fixture
def test_admin(db_session):
    """ Создает тестового администратора """
    user = User(
        email="admin@example.com",
        username="admin",
        role="admin",
        status="active"
    )
    user.set_password("admin123")
    db_session.add(user)
    db_session.commit()
    return user

@pytest.fixture()
def test_motorcycle(db_session, test_user):
    """ Создает тестовый мотоцикл """
    moto = Motorcycle(
        owner_id=test_user.id,
        name="Test Bike",
        years=2020,
        volume=1000,
        mileage=15000,
        color="#FF0000",
        license_plate="0123AB12",
        vin="12345678901234567"
    )
    db_session.add(moto)
    db_session.commit()
    return moto

@pytest.fixture
def auth_headers(test_user):
    """ JWT для авторизованных запросов """
    access_token = create_access_token(identity=str(test_user.id), additional_claims=test_admin.role)
    return { 'Authorization': f'Bearer {access_token}' }

@pytest.fixture
def admin_headers(test_admin):
    """ JWT токен для администратора """
    access_token = create_access_token(identity=str(test_admin.id), additional_claims=test_admin.role)

    return { 'Authorization': f'Bearer {access_token}'}