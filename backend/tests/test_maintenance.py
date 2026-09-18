"""
Тесты домена maintenance: CRUD, complete flow, quick-start.

Регрессии:
- Sprint 2A.1: mark_planned_as_done должен сбрасывать mileage_update reminders
- Sprint 2A.2: mark_planned_as_done обновляет moto.mileage через set_mileage
- Sprint 2A.3: quick_start идёт через MotorcycleService.set_mileage
"""
import pytest

from app.models.maintenance import Maintenance, MaintenanceStatus
from app.models.motorcycle import Motorcycle
from app.models.reminder import Reminder


# ---- Helpers ----

def _create_moto(client, headers, mileage=10000):
    """Создаёт мотоцикл, возвращает JSON."""
    response = client.post(
        "/api/motorcycle/",
        json={"name": "Test Moto", "mileage": mileage},
        headers=headers,
    )
    assert response.status_code == 201, response.get_json()
    return response.get_json()


def _create_planned(client, headers, moto_id, **overrides):
    """Создаёт плановое ТО."""
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


# ---- POST /api/maintenance/ ----

@pytest.mark.maintenance
def test_create_planned_maintenance(client, auth_headers):
    """Создание планового ТО."""
    moto = _create_moto(client, auth_headers)
    data = _create_planned(client, auth_headers, moto["id"])

    assert data["title"] == "Oil change"
    assert data["category"] == "engine"
    assert data["planned_mileage"] == 15000
    assert data["status"] == "planned"
    assert data["moto_id"] == moto["id"]


@pytest.mark.maintenance
def test_create_completed_maintenance(client, auth_headers):
    """Создание уже выполненного ТО."""
    moto = _create_moto(client, auth_headers)
    response = client.post("/api/maintenance/", json={
        "motorcycleId": moto["id"],
        "category": "engine",
        "title": "Oil changed",
        "completed_mileage": 12000,
        "completed_date": "2026-09-01",
        "cost": 3000,
    }, headers=auth_headers)
    assert response.status_code == 201
    data = response.get_json()
    assert data["status"] == "completed"
    assert data["completed_mileage"] == 12000
    assert data["cost"] == 3000


@pytest.mark.maintenance
def test_create_with_both_planned_and_completed_fails(client, auth_headers):
    """Нельзя одновременно planned и completed → 400."""
    moto = _create_moto(client, auth_headers)
    response = client.post("/api/maintenance/", json={
        "motorcycleId": moto["id"],
        "category": "engine",
        "title": "Bad",
        "planned_mileage": 15000,
        "completed_mileage": 12000,
        "completed_date": "2026-09-01",
    }, headers=auth_headers)
    assert response.status_code == 400


@pytest.mark.maintenance
def test_create_completed_without_date_fails(client, auth_headers):
    """completed_mileage без completed_date → 400."""
    moto = _create_moto(client, auth_headers)
    response = client.post("/api/maintenance/", json={
        "motorcycleId": moto["id"],
        "category": "engine",
        "title": "Bad",
        "completed_mileage": 12000,
    }, headers=auth_headers)
    assert response.status_code == 400


@pytest.mark.maintenance
def test_create_for_foreign_moto_forbidden(client, auth_headers, make_user):
    """Создание ТО на чужой мотоцикл → 403."""
    moto = _create_moto(client, auth_headers)

    other = make_user(verified=True)
    login = client.post("/api/auth/login", json={
        "email": other["email"], "password": other["password"], "rememberMe": True,
    }).get_json()
    other_headers = {"Authorization": f"Bearer {login['access_token']}"}

    response = client.post("/api/maintenance/", json={
        "motorcycleId": moto["id"],
        "category": "engine",
        "title": "Hack",
        "planned_mileage": 15000,
    }, headers=other_headers)
    assert response.status_code == 403


# ---- GET ----

@pytest.mark.maintenance
def test_get_maintenances_by_motorcycle(client, auth_headers):
    """Список ТО мотоцикла."""
    moto = _create_moto(client, auth_headers)
    _create_planned(client, auth_headers, moto["id"], title="A")
    _create_planned(client, auth_headers, moto["id"], title="B")

    response = client.get(f"/api/maintenance/motorcycle/{moto['id']}", headers=auth_headers)
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 2
    assert {d["title"] for d in data} == {"A", "B"}


@pytest.mark.maintenance
def test_get_single_maintenance(client, auth_headers):
    """GET /api/maintenance/<id>."""
    moto = _create_moto(client, auth_headers)
    record = _create_planned(client, auth_headers, moto["id"])

    response = client.get(f"/api/maintenance/{record['id']}", headers=auth_headers)
    assert response.status_code == 200
    assert response.get_json()["id"] == record["id"]


@pytest.mark.maintenance
def test_get_nonexistent_maintenance_404(client, auth_headers):
    """GET несуществующего → 404."""
    response = client.get("/api/maintenance/999999", headers=auth_headers)
    assert response.status_code == 404


# ---- PUT ----

@pytest.mark.maintenance
def test_update_maintenance_title_and_cost(client, auth_headers):
    """Обновление title и cost."""
    moto = _create_moto(client, auth_headers)
    record = _create_planned(client, auth_headers, moto["id"])

    response = client.put(
        f"/api/maintenance/{record['id']}",
        json={"title": "Updated title", "cost": 5000},
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["title"] == "Updated title"
    assert data["cost"] == 5000


@pytest.mark.maintenance
def test_update_maintenance_as_completed(client, auth_headers):
    """
    Обновление с completed_mileage и completed_date → статус меняется на completed.

    Регрессия: _recompute_status должен корректно установить status.
    """
    moto = _create_moto(client, auth_headers)
    record = _create_planned(client, auth_headers, moto["id"])

    response = client.put(
        f"/api/maintenance/{record['id']}",
        json={
            "completed_mileage": 12000,
            "completed_date": "2026-09-15",
        },
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "completed"
    assert data["completed_mileage"] == 12000


# ---- DELETE ----

@pytest.mark.maintenance
def test_delete_maintenance(client, auth_headers, db_session):
    """DELETE → 200, запись удалена."""
    moto = _create_moto(client, auth_headers)
    record = _create_planned(client, auth_headers, moto["id"])

    response = client.delete(f"/api/maintenance/{record['id']}", headers=auth_headers)
    assert response.status_code == 200

    assert db_session.session.get(Maintenance, record["id"]) is None


# ---- POST /complete ----

@pytest.mark.maintenance
def test_mark_planned_as_completed(client, auth_headers, db_session):
    """Отметка ТО выполненным без repeat."""
    moto = _create_moto(client, auth_headers, mileage=10000)
    record = _create_planned(client, auth_headers, moto["id"], planned_mileage=15000)

    response = client.post(
        f"/api/maintenance/{record['id']}/complete",
        json={"completed_mileage": 15000, "completed_date": "2026-09-15", "cost": 3000},
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["maintenance"]["status"] == "completed"
    assert data["maintenance"]["completed_mileage"] == 15000
    assert data["new_planned"] is None


@pytest.mark.maintenance
def test_mark_completed_with_repeat_creates_new_planned(client, auth_headers):
    """is_repeat=True + interval → создаётся новое плановое ТО."""
    moto = _create_moto(client, auth_headers, mileage=10000)
    record = _create_planned(client, auth_headers, moto["id"], planned_mileage=15000)

    response = client.post(
        f"/api/maintenance/{record['id']}/complete",
        json={
            "completed_mileage": 15000,
            "completed_date": "2026-09-15",
            "is_repeat": True,
            "interval": 5000,
        },
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["new_planned"] is not None
    assert data["new_planned"]["status"] == "planned"
    assert data["new_planned"]["planned_mileage"] == 20000


@pytest.mark.maintenance
def test_mark_already_completed_fails(client, auth_headers):
    """Повторная отметка completed → 400."""
    moto = _create_moto(client, auth_headers)
    record = _create_planned(client, auth_headers, moto["id"], planned_mileage=15000)

    client.post(
        f"/api/maintenance/{record['id']}/complete",
        json={"completed_mileage": 15000, "completed_date": "2026-09-15"},
        headers=auth_headers,
    )

    response = client.post(
        f"/api/maintenance/{record['id']}/complete",
        json={"completed_mileage": 16000, "completed_date": "2026-09-16"},
        headers=auth_headers,
    )
    assert response.status_code == 400


@pytest.mark.maintenance
def test_complete_updates_moto_mileage_and_clears_reminders(
    client, auth_headers, db_session
):
    """
    Регрессия Sprint 2A.2: при отметке ТО с пробегом > текущего
    moto.mileage обновляется, а pending-напоминания mileage_update
    сбрасываются через MotorcycleService.set_mileage.
    """
    moto = _create_moto(client, auth_headers, mileage=10000)
    record = _create_planned(client, auth_headers, moto["id"], planned_mileage=15000)

    me = client.get("/api/auth/me", headers=auth_headers).get_json()

    reminder = Reminder(
        user_id=me["id"],
        motorcycle_id=moto["id"],
        type=Reminder.TYPE_MILEAGE_UPDATE,
        status=Reminder.STATUS_PENDING,
    )
    db_session.session.add(reminder)
    db_session.session.commit()

    response = client.post(
        f"/api/maintenance/{record['id']}/complete",
        json={"completed_mileage": 15000, "completed_date": "2026-09-15"},
        headers=auth_headers,
    )
    assert response.status_code == 200

    db_moto = db_session.session.get(Motorcycle, moto["id"])
    assert db_moto.mileage == 15000
    assert db_moto.mileage_updated_at is not None

    remaining = db_session.session.query(Reminder).filter_by(
        motorcycle_id=moto["id"],
        type=Reminder.TYPE_MILEAGE_UPDATE,
        status=Reminder.STATUS_PENDING,
    ).count()
    assert remaining == 0


# ---- POST /quick-start ----

@pytest.mark.maintenance
def test_quick_start_success(client, auth_headers, db_session):
    """quick-start создаёт базовый набор плановых ТО."""
    moto = _create_moto(client, auth_headers, mileage=5000)

    response = client.post("/api/maintenance/quick-start", json={
        "moto_id": moto["id"],
        "current_mileage": 5000,
    }, headers=auth_headers)

    assert response.status_code == 201
    data = response.get_json()
    assert "created" in data
    assert len(data["created"]) == 7
    assert "message" in data
    assert data["moto"] is not None

    count = db_session.session.query(Maintenance).filter_by(
        moto_id=moto["id"], status=MaintenanceStatus.PLANNED.value
    ).count()
    assert count == 7


@pytest.mark.maintenance
def test_quick_start_on_moto_with_existing_fails(client, auth_headers):
    """quick-start на мотоцикл с существующими ТО → 400."""
    moto = _create_moto(client, auth_headers)
    _create_planned(client, auth_headers, moto["id"])

    response = client.post("/api/maintenance/quick-start", json={
        "moto_id": moto["id"],
        "current_mileage": 5000,
    }, headers=auth_headers)

    assert response.status_code == 400