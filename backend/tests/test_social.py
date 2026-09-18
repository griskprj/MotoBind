"""
Тесты домена social: посты, лайки, комментарии, репорты.

Регрессии:
- Sprint 5.1: verify actual URL prefix (possible double prefix bug)
- Sprint 5.1: report snapshot has typo 'craeted_at' instead of 'created_at'
"""
import pytest

from app.models.post import Post
from app.models.post_comment import PostComment
from app.models.post_like import PostLike
from app.models.post_report import PostReport


# ---- Helpers ----

def _create_post(client, headers, content="Hello, moto world!"):
    response = client.post(
        "/api/social/posts",
        data={"content": content},
        headers=headers,
    )
    assert response.status_code == 201, response.get_json()
    return response.get_json()


# ---- POST /api/social/posts ----

@pytest.mark.social
def test_create_post_success(client, auth_headers):
    """Создание поста с текстом."""
    data = _create_post(client, auth_headers, content="Test post")

    assert data["content"] == "Test post"
    assert data["is_liked"] is False
    assert data["likes_count"] == 0
    assert data["comments_count"] == 0
    assert "id" in data


@pytest.mark.social
def test_create_post_empty_content(client, auth_headers):
    """Пустой контент → 400."""
    response = client.post(
        "/api/social/posts",
        data={"content": "   "},
        headers=auth_headers,
    )
    assert response.status_code == 400


@pytest.mark.social
def test_create_post_requires_auth(client):
    """Без токена → 401."""
    response = client.post("/api/social/posts", data={"content": "test"})
    assert response.status_code == 401


# ---- GET /api/social/posts ----

@pytest.mark.social
def test_get_posts_empty(client, auth_headers):
    """Пустая лента."""
    response = client.get("/api/social/posts", headers=auth_headers)
    assert response.status_code == 200
    data = response.get_json()
    assert data["posts"] == []
    assert data["total"] == 0


@pytest.mark.social
def test_get_posts_list(client, auth_headers):
    """Список постов."""
    _create_post(client, auth_headers, content="First")
    _create_post(client, auth_headers, content="Second")

    response = client.get("/api/social/posts", headers=auth_headers)
    assert response.status_code == 200
    data = response.get_json()
    assert data["total"] == 2
    assert len(data["posts"]) == 2
    assert data["posts"][0]["content"] == "Second"
    assert data["posts"][1]["content"] == "First"
    assert all("is_liked" in p for p in data["posts"])


@pytest.mark.social
def test_get_posts_by_user_id(client, auth_headers, make_user):
    """Фильтр по user_id."""
    _create_post(client, auth_headers, content="Mine")

    other = make_user(verified=True)
    login = client.post("/api/auth/login", json={
        "email": other["email"], "password": other["password"], "rememberMe": True,
    }).get_json()
    other_headers = {"Authorization": f"Bearer {login['access_token']}"}
    _create_post(client, other_headers, content="Theirs")

    me = client.get("/api/auth/me", headers=auth_headers).get_json()

    response = client.get(
        f"/api/social/posts?user_id={me['id']}",
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["total"] == 1
    assert data["posts"][0]["content"] == "Mine"


# ---- GET /api/social/posts/<id> ----

@pytest.mark.social
def test_get_single_post(client, auth_headers):
    """Получение одного поста."""
    post = _create_post(client, auth_headers)

    response = client.get(f"/api/social/posts/{post['id']}", headers=auth_headers)
    assert response.status_code == 200
    data = response.get_json()
    assert data["id"] == post["id"]
    assert "is_liked" in data


@pytest.mark.social
def test_get_nonexistent_post_404(client, auth_headers):
    """Несуществующий пост → 404."""
    response = client.get("/api/social/posts/999999", headers=auth_headers)
    assert response.status_code == 404


# ---- PUT /api/social/posts/<id> ----

@pytest.mark.social
def test_update_post_content(client, auth_headers):
    """Обновление контента."""
    post = _create_post(client, auth_headers, content="Original")

    response = client.put(
        f"/api/social/posts/{post['id']}",
        data={"content": "Updated"},
        headers=auth_headers,
    )
    assert response.status_code == 200
    assert response.get_json()["content"] == "Updated"


@pytest.mark.social
def test_update_foreign_post_forbidden(client, auth_headers, make_user):
    """Обновление чужого поста → 403."""
    post = _create_post(client, auth_headers)

    other = make_user(verified=True)
    login = client.post("/api/auth/login", json={
        "email": other["email"], "password": other["password"], "rememberMe": True,
    }).get_json()
    other_headers = {"Authorization": f"Bearer {login['access_token']}"}

    response = client.put(
        f"/api/social/posts/{post['id']}",
        data={"content": "Hacked"},
        headers=other_headers,
    )
    assert response.status_code == 403


# ---- DELETE /api/social/posts/<id> ----

@pytest.mark.social
def test_delete_post(client, auth_headers, db_session):
    """Удаление своего поста."""
    post = _create_post(client, auth_headers)

    response = client.delete(f"/api/social/posts/{post['id']}", headers=auth_headers)
    assert response.status_code == 200
    assert db_session.session.get(Post, post["id"]) is None


@pytest.mark.social
def test_delete_foreign_post_forbidden(client, auth_headers, make_user):
    """Удаление чужого поста → 403."""
    post = _create_post(client, auth_headers)

    other = make_user(verified=True)
    login = client.post("/api/auth/login", json={
        "email": other["email"], "password": other["password"], "rememberMe": True,
    }).get_json()
    other_headers = {"Authorization": f"Bearer {login['access_token']}"}

    response = client.delete(f"/api/social/posts/{post['id']}", headers=other_headers)
    assert response.status_code == 403


# ---- POST /api/social/posts/<id>/like ----

@pytest.mark.social
def test_toggle_like_on(client, auth_headers, db_session):
    """Поставить лайк."""
    post = _create_post(client, auth_headers)

    response = client.post(
        f"/api/social/posts/{post['id']}/like",
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["liked"] is True
    assert data["likes_count"] == 1

    assert db_session.session.query(PostLike).filter_by(
        post_id=post["id"]
    ).count() == 1


@pytest.mark.social
def test_toggle_like_off(client, auth_headers):
    """Снять лайк."""
    post = _create_post(client, auth_headers)

    # Ставим
    client.post(f"/api/social/posts/{post['id']}/like", headers=auth_headers)

    # Снимаем
    response = client.post(
        f"/api/social/posts/{post['id']}/like",
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["liked"] is False
    assert data["likes_count"] == 0


@pytest.mark.social
def test_like_on_nonexistent_post_404(client, auth_headers):
    """Лайк на несуществующий пост → 404."""
    response = client.post("/api/social/posts/999999/like", headers=auth_headers)
    assert response.status_code == 404


# ---- POST /api/social/posts/<id>/comments ----

@pytest.mark.social
def test_add_comment(client, auth_headers, db_session):
    """Добавление комментария."""
    post = _create_post(client, auth_headers)

    response = client.post(
        f"/api/social/posts/{post['id']}/comments",
        json={"content": "Nice post!"},
        headers=auth_headers,
    )
    assert response.status_code == 201
    data = response.get_json()
    assert data["content"] == "Nice post!"
    assert data["post_id"] == post["id"]

    db_post = db_session.session.get(Post, post["id"])
    assert db_post.comments_count == 1


@pytest.mark.social
def test_add_empty_comment(client, auth_headers):
    """Пустой комментарий → 400."""
    post = _create_post(client, auth_headers)

    response = client.post(
        f"/api/social/posts/{post['id']}/comments",
        json={"content": "   "},
        headers=auth_headers,
    )
    assert response.status_code == 400


@pytest.mark.social
def test_add_comment_to_nonexistent_post_404(client, auth_headers):
    """Комментарий к несуществующему посту → 404."""
    response = client.post(
        "/api/social/posts/999999/comments",
        json={"content": "test"},
        headers=auth_headers,
    )
    assert response.status_code == 404


# ---- DELETE /api/social/comments/<id> ----

@pytest.mark.social
def test_delete_own_comment(client, auth_headers, db_session):
    """Удаление своего комментария."""
    post = _create_post(client, auth_headers)
    comment = client.post(
        f"/api/social/posts/{post['id']}/comments",
        json={"content": "To delete"},
        headers=auth_headers,
    ).get_json()

    response = client.delete(
        f"/api/social/comments/{comment['id']}",
        headers=auth_headers,
    )
    assert response.status_code == 200
    assert db_session.session.get(PostComment, comment["id"]) is None

    # Счётчик уменьшился
    db_post = db_session.session.get(Post, post["id"])
    assert db_post.comments_count == 0


# ---- POST /api/social/posts/<id>/report ----

@pytest.mark.social
def test_report_post(client, auth_headers, make_user, db_session):
    """Жалоба на чужой пост."""
    other = make_user(verified=True)
    login = client.post("/api/auth/login", json={
        "email": other["email"], "password": other["password"], "rememberMe": True,
    }).get_json()
    other_headers = {"Authorization": f"Bearer {login['access_token']}"}
    post = _create_post(client, other_headers)

    response = client.post(
        f"/api/social/posts/{post['id']}/report",
        json={"category": "spam", "description": "Spam content"},
        headers=auth_headers,
    )
    assert response.status_code == 201
    data = response.get_json()
    assert "report" in data
    assert data["report"]["category"] == "spam"


@pytest.mark.social
def test_report_own_post_fails(client, auth_headers):
    """Жалоба на свой пост → 400."""
    post = _create_post(client, auth_headers)

    response = client.post(
        f"/api/social/posts/{post['id']}/report",
        json={"category": "spam"},
        headers=auth_headers,
    )
    assert response.status_code == 400


@pytest.mark.social
def test_report_invalid_category(client, auth_headers, make_user):
    """Невалидная категория → 400."""
    other = make_user(verified=True)
    login = client.post("/api/auth/login", json={
        "email": other["email"], "password": other["password"], "rememberMe": True,
    }).get_json()
    other_headers = {"Authorization": f"Bearer {login['access_token']}"}
    post = _create_post(client, other_headers)

    response = client.post(
        f"/api/social/posts/{post['id']}/report",
        json={"category": "invalid_category"},
        headers=auth_headers,
    )
    assert response.status_code == 400


@pytest.mark.social
def test_duplicate_report_conflict(client, auth_headers, make_user):
    """Повторная жалоба → 409."""
    other = make_user(verified=True)
    login = client.post("/api/auth/login", json={
        "email": other["email"], "password": other["password"], "rememberMe": True,
    }).get_json()
    other_headers = {"Authorization": f"Bearer {login['access_token']}"}
    post = _create_post(client, other_headers)

    client.post(
        f"/api/social/posts/{post['id']}/report",
        json={"category": "spam"},
        headers=auth_headers,
    )
    response = client.post(
        f"/api/social/posts/{post['id']}/report",
        json={"category": "spam"},
        headers=auth_headers,
    )
    assert response.status_code == 409


# ---- GET /api/social/report-categories ----

@pytest.mark.social
def test_report_categories(client, auth_headers):
    """Список категорий жалоб."""
    response = client.get("/api/social/report-categories", headers=auth_headers)
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == 7
    assert all("value" in c and "label" in c for c in data)