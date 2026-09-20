"""
Тесты домена statistic: гарage, maintenance, repair, registrations.

Покрывает регрессии:
- Sprint 2A.2a: selectinload(User.motorcycle) -> 500 на /api/statistic/repair
- Sprint 3.4: MaintenanceStatus.X vs статус-строка в БД (все счётчики были 0)
"""

import pytest

from app.models.maintenance import MaintenanceStatus

# ---- Helpers ----


def _create_moto(client, headers, name="Test Moto", mileage=10000):
    response = client.post(
        "/api/motorcycle/",
        json={"name": name, "mileage": mileage},
        headers=headers,
    )
    assert response.status_code == 201, response.get_json()
    return response.get_json()


def _create_planned(client, headers, moto_id, **overrides):
    payload = {
        "motorcycleId": moto_id,
        "category": "engine",
        "title": "Oil change",
        "planned_mileage": 15000,
        "planned_date": "2026-10-01",
    }
    payload.update(overrides)
    response = client.post("/api/maintenance/", json=payload, headers=headers)
    assert response.status_code == 201, response.get_json()
    return response.get_json()


def _create_completed(client, headers, moto_id, cost=3000, **overrides):
    payload = {
        "motorcycleId": moto_id,
        "category": "engine",
        "title": "Done",
        "completed_mileage": 12000,
        "completed_date": "2026-09-01",
        "cost": cost,
    }
    payload.update(overrides)
    response = client.post("/api/maintenance/", json=payload, headers=headers)
    assert response.status_code == 201, response.get_json()
    return response.get_json()


# ---- GET /api/statistic/garage ----


@pytest.mark.statistic
def test_garage_stats_empty(client, auth_headers):
    """Пустой гараж → нули."""
    response = client.get("/api/statistic/garage", headers=auth_headers)
    assert response.status_code == 200
    data = response.get_json()
    assert data["motorcycles"] == []
    assert data["cost"] == 0
    assert data["plan_maintenances_count"] == 0
    assert data["maintenances_count"] == 0


@pytest.mark.statistic
def test_garage_stats_with_data(client, auth_headers):
    """
    Гараж с ТО → корректные счётчики.

    Регрессия Sprint 3.4: comparison MaintenanceStatus.X vs str
    делал plan_count/completed_count всегда 0.
    """
    moto = _create_moto(client, auth_headers)
    _create_planned(client, auth_headers, moto["id"])
    _create_completed(client, auth_headers, moto["id"], cost=5000)

    response = client.get("/api/statistic/garage", headers=auth_headers)
    assert response.status_code == 200
    data = response.get_json()

    assert len(data["motorcycles"]) == 1
    assert data["plan_maintenances_count"] == 1
    assert data["maintenances_count"] == 1
    assert data["cost"] == 5000


# ---- GET /api/statistic/garage/<moto_id> ----


@pytest.mark.statistic
def test_moto_garage_stats_empty_maintenances(client, auth_headers):
    """Мото без ТО → пустые списки, нули."""
    moto = _create_moto(client, auth_headers)

    response = client.get(f"/api/statistic/garage/{moto['id']}", headers=auth_headers)
    assert response.status_code == 200
    data = response.get_json()

    assert data["motorcycle"]["id"] == moto["id"]
    assert data["planned_maintenances"] == []
    assert data["recent_maintenances"] == []
    assert data["total_cost"] == 0
    assert data["max_cost"] == 0
    assert data["average_cost"] == 0
    assert data["total_maintenances"] == 0


@pytest.mark.statistic
def test_moto_garage_stats_with_data(client, auth_headers):
    """
    Детальная статистика по мото с ТО.

    Проверяет: подсчёт total_cost, max_cost, average_cost,
    разделение planned / completed.
    """
    moto = _create_moto(client, auth_headers)
    _create_planned(client, auth_headers, moto["id"])
    _create_completed(client, auth_headers, moto["id"], cost=1000)
    _create_completed(client, auth_headers, moto["id"], cost=3000)
    _create_completed(client, auth_headers, moto["id"], cost=5000)

    response = client.get(f"/api/statistic/garage/{moto['id']}", headers=auth_headers)
    assert response.status_code == 200
    data = response.get_json()

    assert len(data["planned_maintenances"]) == 1
    assert len(data["recent_maintenances"]) == 3
    assert data["total_maintenances"] == 3
    assert data["total_cost"] == 9000
    assert data["max_cost"] == 5000
    assert data["average_cost"] == 3000


@pytest.mark.statistic
def test_moto_garage_stats_foreign_moto_forbidden(client, auth_headers, make_user):
    """Чужой мото → 403."""
    moto = _create_moto(client, auth_headers)

    other = make_user(verified=True)
    login = client.post(
        "/api/auth/login",
        json={
            "email": other["email"],
            "password": other["password"],
            "rememberMe": True,
        },
    ).get_json()
    other_headers = {"Authorization": f"Bearer {login['access_token']}"}

    response = client.get(
        f"/api/statistic/garage/{moto['id']}",
        headers=other_headers,
    )
    assert response.status_code == 403


@pytest.mark.statistic
def test_moto_garage_stats_nonexistent_404(client, auth_headers):
    """Несуществующий мото → 404."""
    response = client.get("/api/statistic/garage/999999", headers=auth_headers)
    assert response.status_code == 404


# ---- GET /api/statistic/maintenance ----


@pytest.mark.statistic
def test_maintenance_stats_empty(client, auth_headers):
    """Нет мото → пустой результат."""
    response = client.get("/api/statistic/maintenance", headers=auth_headers)
    assert response.status_code == 200
    data = response.get_json()
    assert data["motorcycles"] == []
    assert data["history_maintenances"] == []
    assert data["planned_maintenances"] == []
    assert data["all_maintenances_count"] == 0


@pytest.mark.statistic
def test_maintenance_stats_split(client, auth_headers):
    """
    Разделение на history и planned.

    Регрессия: сравнение статуса-строки с MaintenanceStatus enum.
    """
    moto = _create_moto(client, auth_headers)
    _create_planned(client, auth_headers, moto["id"])
    _create_completed(client, auth_headers, moto["id"], cost=1000)
    _create_completed(client, auth_headers, moto["id"], cost=2000)

    response = client.get("/api/statistic/maintenance", headers=auth_headers)
    assert response.status_code == 200
    data = response.get_json()

    assert len(data["motorcycles"]) == 1
    assert data["all_maintenances_count"] == 3
    assert len(data["history_maintenances"]) == 2
    assert len(data["planned_maintenances"]) == 1
    assert data["planned_maintenances_count"] == 1
    assert data["overdue_maintenances_count"] == 0

    assert all("moto_name" in m for m in data["history_maintenances"])
    assert all(m["moto_name"] == moto["name"] for m in data["history_maintenances"])


# ---- GET /api/statistic/repair ----


@pytest.mark.statistic
def test_repair_stats_empty(client, auth_headers):
    """
    Пустой случай.

    Регрессия Sprint 2A.2a: selectinload(User.motorcycle)
    падал с LoaderStrategyException → 500.
    """
    response = client.get("/api/statistic/repair", headers=auth_headers)
    assert response.status_code == 200
    data = response.get_json()
    assert data["overdue"] == 0
    assert data["planned"] == 0
    assert data["motorcycles"] == []
    assert data["maintenances"] == []


@pytest.mark.statistic
def test_repair_stats_with_data(client, auth_headers):
    """С данными → корректные счётчики."""
    moto = _create_moto(client, auth_headers)
    _create_planned(client, auth_headers, moto["id"])
    _create_planned(client, auth_headers, moto["id"], title="Second planned")

    response = client.get("/api/statistic/repair", headers=auth_headers)
    assert response.status_code == 200
    data = response.get_json()

    assert data["planned"] == 2
    assert data["overdue"] == 0
    assert len(data["motorcycles"]) == 1
    assert len(data["maintenances"]) == 2
    # Каждая maintenance имеет moto_name
    assert all("moto_name" in m for m in data["maintenances"])


# ---- GET /api/statistic/registrations-chart (admin only) ----


@pytest.mark.statistic
def test_registrations_chart_forbidden_for_user(client, auth_headers):
    """Обычный юзер → 403."""
    response = client.get("/api/statistic/registrations-chart", headers=auth_headers)
    assert response.status_code == 403


@pytest.mark.statistic
def test_registrations_chart_for_admin(client, make_user, db_session):
    """
    Админ → 200 + массив за 12 месяцев.
    """
    from app.models.user import User

    # Создаём админа
    admin = make_user(verified=True)
    db_user = User.query.filter_by(email=admin["email"]).first()
    db_user.role = "admin"
    db_session.session.commit()

    login = client.post(
        "/api/auth/login",
        json={
            "email": admin["email"],
            "password": admin["password"],
            "rememberMe": True,
        },
    ).get_json()
    admin_headers = {"Authorization": f"Bearer {login['access_token']}"}

    response = client.get("/api/statistic/registrations-chart", headers=admin_headers)
    assert response.status_code == 200
    data = response.get_json()

    assert "registrations" in data
    assert len(data["registrations"]) == 12
    assert data["users_count"] >= 1
    assert "last_reg" in data
    assert isinstance(data["last_reg"], list)


# ---- Auth ----


@pytest.mark.statistic
def test_statistic_endpoints_require_auth(client):
    """Все эндпоинты статистики требуют токен."""
    endpoints = [
        "/api/statistic/garage",
        "/api/statistic/maintenance",
        "/api/statistic/repair",
        "/api/statistic/registrations-chart",
    ]
    for endpoint in endpoints:
        response = client.get(endpoint)
        assert response.status_code == 401, f"{endpoint} should require auth"
