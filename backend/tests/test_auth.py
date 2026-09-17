"""
Тесты домена auth: refresh, logout, валидация, password reset.
Smoke-тесты базового флоу — в test_api.py.
"""
import pytest

from app.models.user import User
from app.utils.email import generate_reset_token


# ---- POST /register: валидация ----

@pytest.mark.auth
def test_register_duplicate_username(client, make_user):
    """Регистрация с существующим username → 400."""
    user = make_user()
    response = client.post("/api/auth/register", json={
        "email": "unique@example.com",
        "password": "test123456",
        "username": user["username"],
        "role": "motorcyclist",
    })
    assert response.status_code == 400
    assert "занято" in response.get_json()["error"].lower()


@pytest.mark.auth
def test_register_invalid_email(client):
    """Регистрация с невалидным email → 400 (Pydantic)."""
    response = client.post("/api/auth/register", json={
        "email": "not-an-email",
        "password": "test123456",
        "username": "SomeUser",
        "role": "motorcyclist",
    })
    assert response.status_code == 400


@pytest.mark.auth
def test_register_short_password(client):
    """Регистрация с коротким паролем → 400 (Pydantic)."""
    response = client.post("/api/auth/register", json={
        "email": "short@example.com",
        "password": "123",
        "username": "ShortPass",
        "role": "motorcyclist",
    })
    assert response.status_code == 400


@pytest.mark.auth
def test_register_invalid_role(client):
    """Регистрация с невалидной ролью → 400 (Pydantic)."""
    response = client.post("/api/auth/register", json={
        "email": "badrole@example.com",
        "password": "test123456",
        "username": "BadRole",
        "role": "admin",
    })
    assert response.status_code == 400


# ---- POST /login: edge cases ----

@pytest.mark.auth
def test_login_nonexistent_email(client):
    """Логин с несуществующим email → 404."""
    response = client.post("/api/auth/login", json={
        "email": "ghost@example.com",
        "password": "test123456",
        "rememberMe": True,
    })
    assert response.status_code == 404


@pytest.mark.auth
def test_login_banned_user(client, make_user, db_session):
    """Логин забаненного → 403."""
    user = make_user(verified=True)
    db_user = User.query.filter_by(email=user["email"]).first()
    db_user.status = "banned"
    db_session.session.commit()

    response = client.post("/api/auth/login", json={
        "email": user["email"],
        "password": user["password"],
        "rememberMe": True,
    })
    assert response.status_code == 403


@pytest.mark.auth
def test_login_without_remember_me(client, make_user):
    """rememberMe=false → refresh_token=None в ответе."""
    user = make_user(verified=True)
    response = client.post("/api/auth/login", json={
        "email": user["email"],
        "password": user["password"],
        "rememberMe": False,
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data["access_token"]
    assert data["refresh_token"] is None


# ---- POST /refresh ----

@pytest.mark.auth
def test_refresh_success(client, make_user):
    """Валидный refresh_token → новые access+refresh."""
    user = make_user(verified=True)
    login = client.post("/api/auth/login", json={
        "email": user["email"],
        "password": user["password"],
        "rememberMe": True,
    }).get_json()

    response = client.post("/api/auth/refresh", json={
        "refresh_token": login["refresh_token"],
    })
    assert response.status_code == 200
    data = response.get_json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["refresh_token"] != login["refresh_token"]


@pytest.mark.auth
def test_refresh_invalid_token(client):
    """Невалидный refresh_token → 401."""
    response = client.post("/api/auth/refresh", json={
        "refresh_token": "totally-invalid-token",
    })
    assert response.status_code == 401


@pytest.mark.auth
def test_refresh_missing_token(client):
    """Пустой refresh_token → 400 (Pydantic min_length=1)."""
    response = client.post("/api/auth/refresh", json={
        "refresh_token": "",
    })
    assert response.status_code == 400


# ---- POST /logout ----

@pytest.mark.auth
def test_logout_clears_refresh_token(client, make_user, db_session):
    """Logout → refresh_token очищен в БД."""
    user = make_user(verified=True)
    login = client.post("/api/auth/login", json={
        "email": user["email"],
        "password": user["password"],
        "rememberMe": True,
    }).get_json()

    response = client.post("/api/auth/logout", headers={
        "Authorization": f"Bearer {login['access_token']}",
    })
    assert response.status_code == 200

    db_user = User.query.filter_by(email=user["email"]).first()
    assert db_user.refresh_token is None


@pytest.mark.auth
def test_logout_requires_auth(client):
    """Logout без токена → 401."""
    response = client.post("/api/auth/logout")
    assert response.status_code == 401


# ---- Password reset ----

@pytest.mark.auth
def test_forgot_password_nonexistent_email(client):
    """Forgot password для несуществующего email → 200 (не раскрываем)."""
    response = client.post("/api/auth/forgot-password", json={
        "email": "ghost@example.com",
    })
    assert response.status_code == 200


@pytest.mark.auth
def test_forgot_password_missing_email(client):
    """Forgot password без email → 400."""
    response = client.post("/api/auth/forgot-password", json={})
    assert response.status_code == 400


@pytest.mark.auth
def test_reset_password_invalid_token(client):
    """Reset password с невалидным токеном → 400."""
    response = client.post("/api/auth/reset-password", json={
        "token": "invalid-token",
        "new_password": "newpass123",
    })
    assert response.status_code == 400


@pytest.mark.auth
def test_reset_password_success(client, make_user, db_session):
    """Reset password с валидным токеном → пароль меняется."""
    user = make_user(verified=True)

    token = generate_reset_token(user["email"])

    response = client.post("/api/auth/reset-password", json={
        "token": token,
        "new_password": "newpass12345",
    })
    assert response.status_code == 200

    old_pass_login = client.post("/api/auth/login", json={
        "email": user["email"],
        "password": user["password"],
        "rememberMe": True,
    })
    assert old_pass_login.status_code == 403

    new_pass_login = client.post("/api/auth/login", json={
        "email": user["email"],
        "password": "newpass12345",
        "rememberMe": True,
    })
    assert new_pass_login.status_code == 200


@pytest.mark.auth
def test_reset_password_short_password(client):
    """Reset password с коротким паролем → 400."""
    response = client.post("/api/auth/reset-password", json={
        "token": "any-token",
        "new_password": "123",
    })
    assert response.status_code == 400


@pytest.mark.auth
def test_check_reset_token_valid(client, make_user):
    """check-reset-token с валидным токеном → valid=true."""
    user = make_user(verified=True)
    token = generate_reset_token(user["email"])

    response = client.get(f"/api/auth/check-reset-token/{token}")
    assert response.status_code == 200
    data = response.get_json()
    assert data["valid"] is True
    assert data["email"] == user["email"]


@pytest.mark.auth
def test_check_reset_token_invalid(client):
    """check-reset-token с мусором → 400."""
    response = client.get("/api/auth/check-reset-token/invalid-token")
    assert response.status_code == 400