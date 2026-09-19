"""
Тесты домена manuals: CRUD, модерация, шаги, поиск.

Регрессии:
- Sprint 6.1: hardcoded admin check (current_user_id == 1) в get_manual_by_id
- Sprint 6.1: user cannot filter own moderate/rejected manuals out (missing status filter)
"""
import json

import pytest

from app.models.manual import Manual, ManualStep
from app.models.user import User


# ---- Helpers ----

def _create_manual_payload(**overrides):
    """Payload для CreateManualSchema."""
    payload = {
        "title": "Замена масла",
        "description": "Пошаговая инструкция",
        "category": "engine",
        "difficult": "easy",
        "motorcycle": "Yamaha MT-07",
        "steps": [
            {"order": 1, "title": "Слить старое масло"},
            {"order": 2, "title": "Залить новое"},
        ],
    }
    payload.update(overrides)
    return payload


def _create_manual(client, headers, **overrides):
    """Создаёт мануал через API, возвращает JSON."""
    payload = _create_manual_payload(**overrides)
    response = client.post(
        "/api/manual/new-manual",
        data={"data": json.dumps(payload)},
        headers=headers,
        content_type="multipart/form-data",
    )
    assert response.status_code == 201, response.get_json()
    return response.get_json()


def _make_admin(client, make_user, db_session):
    """Создаёт админа, логинит, возвращает headers."""
    admin = make_user(verified=True)
    db_user = User.query.filter_by(email=admin["email"]).first()
    db_user.role = "admin"
    db_session.session.commit()

    login = client.post("/api/auth/login", json={
        "email": admin["email"],
        "password": admin["password"],
        "rememberMe": True,
    }).get_json()
    return {"Authorization": f"Bearer {login['access_token']}"}, db_user.id


# ---- POST /api/manual/new-manual ----

@pytest.mark.manuals
def test_create_manual_success(client, auth_headers):
    """Создание мануала с шагами."""
    data = _create_manual(client, auth_headers)

    assert data["title"] == "Замена масла"
    assert data["category"] == "engine"
    assert data["motorcycle"] == "Yamaha MT-07"
    assert data["status"] == "moderate"
    assert len(data["steps"]) == 2
    assert data["steps"][0]["order"] == 1


@pytest.mark.manuals
def test_create_manual_missing_data(client, auth_headers):
    """Без поля data → 400."""
    response = client.post(
        "/api/manual/new-manual",
        data={},
        headers=auth_headers,
    )
    assert response.status_code == 400


@pytest.mark.manuals
def test_create_manual_invalid_json(client, auth_headers):
    """Невалидный JSON → 400."""
    response = client.post(
        "/api/manual/new-manual",
        data={"data": "not-json{{{"},
        headers=auth_headers,
    )
    assert response.status_code == 400


@pytest.mark.manuals
def test_create_manual_empty_steps(client, auth_headers):
    """Пустой список шагов → 400 (min_length=1)."""
    payload = _create_manual_payload(steps=[])
    response = client.post(
        "/api/manual/new-manual",
        data={"data": json.dumps(payload)},
        headers=auth_headers,
        content_type="multipart/form-data",
    )
    assert response.status_code == 400


@pytest.mark.manuals
def test_create_manual_invalid_difficult(client, auth_headers):
    """Невалидная сложность → 400."""
    payload = _create_manual_payload(difficult="impossible")
    response = client.post(
        "/api/manual/new-manual",
        data={"data": json.dumps(payload)},
        headers=auth_headers,
        content_type="multipart/form-data",
    )
    assert response.status_code == 400


@pytest.mark.manuals
def test_create_manual_non_sequential_steps(client, auth_headers):
    """Порядок шагов не 1,2,3... → 400."""
    payload = _create_manual_payload(steps=[
        {"order": 1, "title": "First"},
        {"order": 3, "title": "Third"},
    ])
    response = client.post(
        "/api/manual/new-manual",
        data={"data": json.dumps(payload)},
        headers=auth_headers,
        content_type="multipart/form-data",
    )
    assert response.status_code == 400


# ---- GET /api/manual/list ----

@pytest.mark.manuals
def test_list_manuals_empty(client, auth_headers):
    """Пустой список."""
    response = client.get("/api/manual/list", headers=auth_headers)
    assert response.status_code == 200
    data = response.get_json()
    assert data["manuals"] == []
    assert data["total"] == 0


@pytest.mark.manuals
def test_list_manuals_all(client, auth_headers, make_user, db_session):
    """Список всех approved мануалов."""
    other = make_user(verified=True)
    login = client.post("/api/auth/login", json={
        "email": other["email"], "password": other["password"], "rememberMe": True,
    }).get_json()
    other_headers = {"Authorization": f"Bearer {login['access_token']}"}

    manual = _create_manual(client, other_headers, title="Other manual")

    db_manual = db_session.session.get(Manual, manual["id"])
    db_manual.status = "approved"
    db_session.session.commit()

    response = client.get("/api/manual/list", headers=auth_headers)
    assert response.status_code == 200
    data = response.get_json()
    assert data["total"] == 1
    assert data["manuals"][0]["title"] == "Other manual"


@pytest.mark.manuals
def test_list_manuals_tab_my(client, auth_headers, make_user):
    """tab=my → только свои мануалы."""
    _create_manual(client, auth_headers, title="Mine")

    other = make_user(verified=True)
    login = client.post("/api/auth/login", json={
        "email": other["email"], "password": other["password"], "rememberMe": True,
    }).get_json()
    other_headers = {"Authorization": f"Bearer {login['access_token']}"}
    _create_manual(client, other_headers, title="Theirs")

    response = client.get("/api/manual/list?tab=my", headers=auth_headers)
    assert response.status_code == 200
    data = response.get_json()
    assert data["total"] == 1
    assert data["manuals"][0]["title"] == "Mine"


@pytest.mark.manuals
def test_list_manuals_search(client, auth_headers):
    """Поиск по title."""
    _create_manual(client, auth_headers, title="Замена масла")
    _create_manual(client, auth_headers, title="Регулировка цепи")

    response = client.get("/api/manual/list?search=масла", headers=auth_headers)
    assert response.status_code == 200
    data = response.get_json()
    assert data["total"] == 1
    assert data["manuals"][0]["title"] == "Замена масла"


@pytest.mark.manuals
def test_list_manuals_filter_by_category(client, auth_headers):
    """Фильтр по категории."""
    _create_manual(client, auth_headers, title="A", category="engine")
    _create_manual(client, auth_headers, title="B", category="brakes")

    response = client.get("/api/manual/list?category=engine", headers=auth_headers)
    assert response.status_code == 200
    data = response.get_json()
    assert data["total"] == 1
    assert data["manuals"][0]["category"] == "engine"


# ---- GET /api/manual/<id> ----

@pytest.mark.manuals
def test_get_approved_manual_by_any_user(client, auth_headers, make_user, db_session):
    """Approved мануал виден всем."""
    other = make_user(verified=True)
    login = client.post("/api/auth/login", json={
        "email": other["email"], "password": other["password"], "rememberMe": True,
    }).get_json()
    other_headers = {"Authorization": f"Bearer {login['access_token']}"}
    manual = _create_manual(client, other_headers)

    db_manual = db_session.session.get(Manual, manual["id"])
    db_manual.status = "approved"
    db_session.session.commit()

    # Другой юзер видит
    response = client.get(f"/api/manual/{manual['id']}", headers=auth_headers)
    assert response.status_code == 200


@pytest.mark.manuals
def test_get_own_moderate_manual(client, auth_headers):
    """Автор видит свой moderate мануал."""
    manual = _create_manual(client, auth_headers)

    response = client.get(f"/api/manual/{manual['id']}", headers=auth_headers)
    assert response.status_code == 200


@pytest.mark.manuals
def test_get_foreign_moderate_manual_forbidden(client, auth_headers, make_user):
    """Чужой moderate мануал → 403."""
    manual = _create_manual(client, auth_headers)

    other = make_user(verified=True)
    login = client.post("/api/auth/login", json={
        "email": other["email"], "password": other["password"], "rememberMe": True,
    }).get_json()
    other_headers = {"Authorization": f"Bearer {login['access_token']}"}

    response = client.get(f"/api/manual/{manual['id']}", headers=other_headers)
    assert response.status_code == 403


@pytest.mark.manuals
def test_admin_can_see_any_moderate_manual(client, make_user, db_session):
    """
    Админ видит любой moderate мануал.

    Регрессия Sprint 6.1: hardcoded is_admin = (current_user_id == 1).
    """
    # Автор — обычный юзер
    author = make_user(verified=True)
    login_author = client.post("/api/auth/login", json={
        "email": author["email"], "password": author["password"], "rememberMe": True,
    }).get_json()
    author_headers = {"Authorization": f"Bearer {login_author['access_token']}"}
    manual = _create_manual(client, author_headers)

    # Админ — другой юзер (id != 1)
    admin_headers, admin_id = _make_admin(client, make_user, db_session)

    response = client.get(f"/api/manual/{manual['id']}", headers=admin_headers)
    assert response.status_code == 200, (
        f"Admin (id={admin_id}) should see moderate manual, "
        f"but got {response.status_code}. "
        f"Bug: is_admin hardcoded to current_user_id == 1."
    )


@pytest.mark.manuals
def test_get_nonexistent_manual_404(client, auth_headers):
    """Несуществующий мануал → 404."""
    response = client.get("/api/manual/999999", headers=auth_headers)
    assert response.status_code == 404


# ---- PUT /api/manual/<id> ----

@pytest.mark.manuals
def test_update_own_moderate_manual(client, auth_headers):
    """Автор не может редактировать moderate мануал."""
    manual = _create_manual(client, auth_headers)

    response = client.put(
        f"/api/manual/{manual['id']}",
        json={"title": "Обновлённый заголовок"},
        headers=auth_headers,
    )
    assert response.status_code == 403

@pytest.mark.manuals
def test_update_own_approved_manual_forbidden(client, auth_headers):
    """Автор не может редактировать approved мануал."""
    manual = _create_manual(client, auth_headers)

    response = client.put(
        f"/api/manual/{manual['id']}",
        json={"title": "Обновленный заголовок"},
        headers=auth_headers,
    )
    assert response.status_code == 403


@pytest.mark.manuals
def test_update_own_rejected_manual_resets_to_moderate(client, auth_headers, db_session):
    """Автор редактирует rejected мануал → статус обратно moderate."""
    manual = _create_manual(client, auth_headers)
    db_manual = db_session.session.get(Manual, manual["id"])
    db_manual.status = "rejected"
    db_manual.rejection_reason = "Плохое качество"
    db_session.session.commit()

    response = client.put(
        f"/api/manual/{manual['id']}",
        json={"title": "Improved"},
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "moderate"


# ---- DELETE /api/manual/<id> ----

@pytest.mark.manuals
def test_delete_own_manual(client, auth_headers, db_session):
    """Удаление своего мануала."""
    manual = _create_manual(client, auth_headers)

    response = client.delete(f"/api/manual/{manual['id']}", headers=auth_headers)
    assert response.status_code == 200
    assert db_session.session.get(Manual, manual["id"]) is None


@pytest.mark.manuals
def test_delete_foreign_manual_forbidden(client, auth_headers, make_user):
    """Удаление чужого мануала → 403."""
    manual = _create_manual(client, auth_headers)

    other = make_user(verified=True)
    login = client.post("/api/auth/login", json={
        "email": other["email"], "password": other["password"], "rememberMe": True,
    }).get_json()
    other_headers = {"Authorization": f"Bearer {login['access_token']}"}

    response = client.delete(f"/api/manual/{manual['id']}", headers=other_headers)
    assert response.status_code == 403


# ---- Steps ----

@pytest.mark.manuals
def test_update_manual_replaces_steps(client, auth_headers, db_session):
    """
    PUT со steps заменяет все шаги (на rejected мануале).

    Moderate мануалы редактировать нельзя (см. test_update_own_moderate_manual_forbidden).
    """
    manual = _create_manual(client, auth_headers)
    assert len(manual["steps"]) == 2

    db_manual = db_session.session.get(Manual, manual["id"])
    db_manual.status = "rejected"
    db_session.session.commit()

    response = client.put(
        f"/api/manual/{manual['id']}",
        json={"steps": [
            {"order": 1, "title": "Новый шаг 1"},
            {"order": 2, "title": "Новый шаг 2"},
            {"order": 3, "title": "Новый шаг 3"},
        ]},
        headers=auth_headers,
    )
    assert response.status_code == 200

    steps = ManualStep.query.filter_by(manual_id=manual["id"]).all()
    assert len(steps) == 3
    assert {s.title for s in steps} == {"Новый шаг 1", "Новый шаг 2", "Новый шаг 3"}


# ---- Auth ----

@pytest.mark.manuals
def test_manuals_endpoints_require_auth(client):
    """Без токена → 401."""
    endpoints = [
        "/api/manual/list",
        "/api/manual/1",
    ]
    for endpoint in endpoints:
        response = client.get(endpoint)
        assert response.status_code == 401, f"{endpoint} should require auth"