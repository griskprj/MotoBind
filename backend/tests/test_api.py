"""
Smoke-тесты API: проверяют, что базовые ручки работают.
Детальные тесты по доменам — в test_auth.py, test_motorcycle.py и т.д.
"""


def test_register(client, db_session):
    """Регистрация возвращает токены и user, requires_verification=True."""
    response = client.post(
        "/api/auth/register",
        json={
            "email": "register@example.com",
            "password": "test123456",
            "username": "RegisterUser",
            "role": "motorcyclist",
        },
    )
    assert response.status_code == 201
    data = response.get_json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["user"]["email"] == "register@example.com"
    assert data["user"]["username"] == "RegisterUser"
    assert data["requires_verification"] is True


def test_register_duplicate_email(client, make_user):
    """Регистрация с существующим email → 400."""
    user = make_user()
    response = client.post(
        "/api/auth/register",
        json={
            "email": user["email"],
            "password": "otherpass123",
            "username": "OtherUser",
            "role": "motorcyclist",
        },
    )
    assert response.status_code == 400


def test_login_unverified_fails(client, make_user):
    """Логин без подтверждённого email → 403."""
    user = make_user()  # verified=False
    response = client.post(
        "/api/auth/login",
        json={
            "email": user["email"],
            "password": user["password"],
            "rememberMe": True,
        },
    )
    assert response.status_code == 403
    assert "подтвержд" in response.get_json()["error"].lower()


def test_login_success(client, make_user):
    """Логин подтверждённого пользователя → 200 + токены."""
    user = make_user(verified=True)
    response = client.post(
        "/api/auth/login",
        json={
            "email": user["email"],
            "password": user["password"],
            "rememberMe": True,
        },
    )
    assert response.status_code == 200
    data = response.get_json()
    assert "access_token" in data
    assert data["refresh_token"] is not None


def test_login_wrong_password(client, make_user):
    """Логин с неверным паролем → 403."""
    user = make_user(verified=True)
    response = client.post(
        "/api/auth/login",
        json={
            "email": user["email"],
            "password": "wrong_password",
            "rememberMe": True,
        },
    )
    assert response.status_code == 403


def test_me_endpoint(client, auth_headers):
    """GET /api/auth/me возвращает текущего пользователя."""
    response = client.get("/api/auth/me", headers=auth_headers)
    assert response.status_code == 200
    data = response.get_json()
    assert data["email"].startswith("user")
    assert data["role"] == "motorcyclist"
