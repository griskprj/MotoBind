"""
Тесты домена motorcycle: CRUD, permissions, валидация.

Покрывает регрессии:
- Sprint 0: owner_required (несуществующий объект → 404, не 500)
- Sprint 1: licensePlate (camelCase в схеме, snake_case в модели)
"""
import pytest

from app.models.motorcycle import Motorcycle
from app.models.reminder import Reminder
from app.models.user import User


# ---- Helpers ----

def _create_moto(client, headers, **overrides):
    """Создаёт мотоцикл через API, возвращает JSON."""
    payload = {
        "name": "Yamaha MT-07",
        "years": 2020,
        "volume": 689,
        "mileage": 15000,
        "color": "#FF0000",
        "licensePlate": "А123БВ777",
        "vin": "JYARM33E000123456",
    }
    payload.update(overrides)
    response = client.post("/api/motorcycle/", json=payload, headers=headers)
    assert response.status_code == 201, f"create failed: {response.get_json()}"
    return response.get_json()


# ---- CRUD ----

@pytest.mark.motorcycle
def test_create_motorcycle_minimal(client, auth_headers):
    """Минимальный набор полей: только name."""
    response = client.post(
        "/api/motorcycle/",
        json={"name": "Honda CB500"},
        headers=auth_headers,
    )
    assert response.status_code == 201
    data = response.get_json()
    assert data["name"] == "Honda CB500"
    assert data["mileage"] == 0
    assert "id" in data


@pytest.mark.motorcycle
def test_create_motorcycle_full(client, auth_headers):
    """Все поля."""
    data = _create_moto(client, auth_headers)
    assert data["name"] == "Yamaha MT-07"
    assert data["years"] == 2020
    assert data["volume"] == 689
    assert data["mileage"] == 15000
    assert data["color"] == "#FF0000"
    assert data["license_plate"] == "А123БВ777"
    assert data["vin"] == "JYARM33E000123456"


@pytest.mark.motorcycle
def test_get_user_motorcycles_empty(client, auth_headers):
    """Пустой гараж → пустой список."""
    response = client.get("/api/motorcycle/", headers=auth_headers)
    assert response.status_code == 200
    assert response.get_json() == []


@pytest.mark.motorcycle
def test_get_user_motorcycles_list(client, auth_headers):
    """Список возвращает все мотоциклы пользователя."""
    _create_moto(client, auth_headers, name="Moto A")
    _create_moto(client, auth_headers, name="Moto B")

    response = client.get("/api/motorcycle/", headers=auth_headers)
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 2
    names = {m["name"] for m in data}
    assert names == {"Moto A", "Moto B"}
    assert all("maintenances" in m for m in data)


@pytest.mark.motorcycle
def test_update_motorcycle_name(client, auth_headers):
    """Обновление имени."""
    moto = _create_moto(client, auth_headers)
    response = client.put(
        f"/api/motorcycle/{moto['id']}",
        json={"name": "Yamaha MT-09"},
        headers=auth_headers,
    )
    assert response.status_code == 200
    assert response.get_json()["name"] == "Yamaha MT-09"


@pytest.mark.motorcycle
def test_update_motorcycle_license_plate(client, auth_headers, db_session):
    """
    Регрессия Sprint 1: licensePlate молча игнорировался.

    Фронт шлёт camelCase, схема должна конвертировать в snake_case,
    сервис должен найти поле в модели и обновить.
    """
    moto = _create_moto(client, auth_headers)

    new_plate = "В999ЕК196"
    response = client.put(
        f"/api/motorcycle/{moto['id']}",
        json={"licensePlate": new_plate},
        headers=auth_headers,
    )
    assert response.status_code == 200
    assert response.get_json()["license_plate"] == new_plate

    db_moto = db_session.session.get(Motorcycle, moto["id"])
    assert db_moto.license_plate == new_plate


@pytest.mark.motorcycle
def test_update_motorcycle_mileage(client, auth_headers, db_session):
    """PATCH пробега → mileage обновлён, mileage_updated_at выставлен."""
    moto = _create_moto(client, auth_headers, mileage=10000)
    old_updated_at = db_session.session.get(Motorcycle, moto["id"]).mileage_updated_at

    response = client.patch(
        f"/api/motorcycle/{moto['id']}",
        json={"mileage": 20000},
        headers=auth_headers,
    )
    assert response.status_code == 200
    assert response.get_json()["mileage"] == 20000

    db_moto = db_session.session.get(Motorcycle, moto["id"])
    assert db_moto.mileage == 20000
    assert db_moto.mileage_updated_at is not None
    if old_updated_at:
        assert db_moto.mileage_updated_at != old_updated_at


@pytest.mark.motorcycle
def test_update_mileage_clears_pending_reminder(client, auth_headers, db_session, make_user):
    """При обновлении пробега pending-напоминания mileage_update удаляются."""
    moto = _create_moto(client, auth_headers)

    me = client.get("/api/auth/me", headers=auth_headers).get_json()

    reminder = Reminder(
        user_id=me["id"],
        motorcycle_id=moto["id"],
        type=Reminder.TYPE_MILEAGE_UPDATE,
        status=Reminder.STATUS_PENDING,
    )
    db_session.session.add(reminder)
    db_session.session.commit()
    assert db_session.session.query(Reminder).count() == 1

    response = client.patch(
        f"/api/motorcycle/{moto['id']}",
        json={"mileage": 50000},
        headers=auth_headers,
    )
    assert response.status_code == 200

    remaining = db_session.session.query(Reminder).filter_by(
        motorcycle_id=moto["id"],
        type=Reminder.TYPE_MILEAGE_UPDATE,
        status=Reminder.STATUS_PENDING,
    ).count()
    assert remaining == 0


@pytest.mark.motorcycle
def test_update_note(client, auth_headers):
    """Обновление заметок."""
    moto = _create_moto(client, auth_headers)
    response = client.patch(
        f"/api/motorcycle/{moto['id']}/note",
        json={"note": "Купил новые шины"},
        headers=auth_headers,
    )
    assert response.status_code == 200
    assert response.get_json()["note"] == "Купил новые шины"


@pytest.mark.motorcycle
def test_update_note_too_long(client, auth_headers):
    """Заметка > 128 символов → 400."""
    moto = _create_moto(client, auth_headers)
    response = client.patch(
        f"/api/motorcycle/{moto['id']}/note",
        json={"note": "x" * 200},
        headers=auth_headers,
    )
    assert response.status_code == 400


@pytest.mark.motorcycle
def test_delete_motorcycle(client, auth_headers, db_session):
    """DELETE → 200, мото исчезает из БД."""
    moto = _create_moto(client, auth_headers)
    moto_id = moto["id"]

    response = client.delete(f"/api/motorcycle/{moto_id}", headers=auth_headers)
    assert response.status_code == 200

    assert db_session.session.get(Motorcycle, moto_id) is None


# ---- Permissions ----

@pytest.mark.motorcycle
def test_get_other_user_motorcycle_forbidden(client, auth_headers, make_user):
    """Обновление чужого мото → 403."""
    moto = _create_moto(client, auth_headers)

    other_user = make_user(verified=True)
    login = client.post("/api/auth/login", json={
        "email": other_user["email"],
        "password": other_user["password"],
        "rememberMe": True,
    }).get_json()
    other_headers = {"Authorization": f"Bearer {login['access_token']}"}

    response = client.put(
        f"/api/motorcycle/{moto['id']}",
        json={"name": "Hacked"},
        headers=other_headers,
    )
    assert response.status_code == 403


@pytest.mark.motorcycle
def test_update_nonexistent_motorcycle_404(client, auth_headers):
    """
    Регрессия Sprint 0: owner_required падал с 500, если объекта нет.

    Ожидаем 404, не 500.
    """
    response = client.put(
        "/api/motorcycle/999999",
        json={"name": "Ghost"},
        headers=auth_headers,
    )
    assert response.status_code == 404


@pytest.mark.motorcycle
def test_delete_nonexistent_motorcycle_404(client, auth_headers):
    """DELETE несуществующего → 404."""
    response = client.delete("/api/motorcycle/999999", headers=auth_headers)
    assert response.status_code == 404


@pytest.mark.motorcycle
def test_motorcycle_requires_auth(client):
    """Без токена → 401."""
    response = client.get("/api/motorcycle/")
    assert response.status_code == 401


# ---- Валидация ----

@pytest.mark.motorcycle
def test_create_invalid_vin(client, auth_headers):
    """VIN != 17 символов → 400."""
    response = client.post(
        "/api/motorcycle/",
        json={"name": "Test", "vin": "SHORTVIN"},
        headers=auth_headers,
    )
    assert response.status_code == 400


@pytest.mark.motorcycle
def test_create_invalid_color(client, auth_headers):
    """Color не HEX → 400."""
    response = client.post(
        "/api/motorcycle/",
        json={"name": "Test", "color": "red"},
        headers=auth_headers,
    )
    assert response.status_code == 400


@pytest.mark.motorcycle
def test_create_invalid_license_plate(client, auth_headers):
    """License plate не 8-9 символов → 400."""
    response = client.post(
        "/api/motorcycle/",
        json={"name": "Test", "licensePlate": "AB"},
        headers=auth_headers,
    )
    assert response.status_code == 400

@pytest.mark.motorcycle
def test_validation_error_is_json_serializable(client, auth_headers):
    """
    Регрессия Sprint 3.2: обработчик ошибок Pydantic падал с 500
    из-за не-JSON-сериализуемого ValueError в ctx.

    Ожидаем корректный 400 с JSON телом.
    """
    response = client.post(
        "/api/motorcycle/",
        json={"name": "Test", "vin": "SHORT"},
        headers=auth_headers,
    )
    assert response.status_code == 400

    data = response.get_json()
    assert data is not None
    assert data["error"] == "Ошибка валидации"
    assert "errors" in data
    locs = [tuple(e["loc"]) for e in data["errors"]]
    assert ("vin",) in locs