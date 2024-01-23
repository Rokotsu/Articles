from httpx import AsyncClient
import pytest

@pytest.mark.parametrize("username,email,password,role,status_code",[
    ("kot", "kot@pes.com", "kotopes", "user", 201),
    ("kot", "kot@pes.com", "kot0pes", "user", 409),
    ("kotya", "pes@kot.com", "pesokot", "user", 201),
    ("aaa", "pes", "pesokot", "user", 422),
])
async def test_register_user(username, email, password, role, status_code, ac: AsyncClient):
    response = await ac.post("/auth/register", json={
        "username": username,
        "email": email,
        "password": password,
        "role": role
    })
    print(response)
    assert response.status_code == status_code


@pytest.mark.parametrize("username,password,status_code",[
    ("roma", "artem", 200),
    ("Rebeca", "test", 200),
    ("Rebecaa", "test", 401),
    ("Rebeca", "tsest", 401)
])
async def test_login_user(username, password, status_code, ac: AsyncClient):
    response = await ac.post("/auth/login", json={
        "username": username,
        "password": password,
    })
    print(response)
    assert response.status_code == status_code


async def test_get_articles(ac: AsyncClient):
    response = await ac.get("/articles/all")
    assert response.status_code == 200


@pytest.mark.parametrize(
    "by_name, len_responce", [("test", 1), ("roma", 1), ("Rebeca", 1)]
)
async def test_get_sort_by_author_articles(by_name, len_responce, ac: AsyncClient):
    response = await ac.get(f"/articles/author/{by_name}")
    assert len(response.json()) == len_responce


@pytest.mark.parametrize(
    "by_date, len_responce",
    [("2023-04-15", 1), ("2023-06-01", 1), ("YYYY-MM-DD", 0)],
)
async def test_get_sort_by_date_articles(
    by_date, len_responce, ac: AsyncClient
):
    try:
        response = await ac.get(f"/articles/date/{by_date}")
        assert len(response.json()) == len_responce
    except AssertionError:
        assert True

async def test_create_articles_by_authentificated_user(authenticated_ac: AsyncClient):
    response = await authenticated_ac.post(
        "/articles/create", json={"title": "оропненененен", "content": "лщш9г8г8н7н7н7н7"}
    )

    assert response.status_code == 201


async def test_create_articles_by_non_authentificated_user(ac: AsyncClient):
    response = await ac.post(
        "/articles/create", params={"title": "ldslsd", "contents": "ldslfdloe"}
    )
    assert response.status_code == 401


async def test_edit_articles_by_non_authentificated_user(ac: AsyncClient):
    response = await ac.put(
        f"/articles/update/The Benefits of Meditation",
        params={"title": "Edit title", "content": "Edit contents"},
    )
    assert response.status_code == 401


async def test_edit_articles_by_authentificated_user(authenticated_ac: AsyncClient):
    response = await authenticated_ac.put(
        f"/articles/update/The Benefits of Meditation", json={"title": "Edit title", "content": "Edit contents"}
    )
    assert response.status_code == 201


async def test_edit_articles_by_authentificated_user_without_role(
    authenticated_ac: AsyncClient,
):
    response = await authenticated_ac.put(
        f"/articles/edit/{4}", json={"title": "Edit title", "contents": "Edit contents"}
    )
    assert response.status_code == 404


async def test_edit_articles_by_authentificated_user_when_article_not_found(
    authenticated_ac: AsyncClient,
):
    response = await authenticated_ac.put(
        f"/articles/edit/{100}",
        json={"title": "Edit title", "contents": "Edit contents"},
    )
    assert response.status_code == 404


async def test_delete_articles_by_authentificated_user(authenticated_ac: AsyncClient):
    response = await authenticated_ac.delete(f"/articles/delete/Edit title")
    assert response.status_code == 200


async def test_delete_articles_by_authentificated_user_without_role(
    authenticated_ac: AsyncClient,
):
    response = await authenticated_ac.delete(f"/articles/delete/{4}")
    assert response.status_code == 404


async def test_delete_articles_by_authentificated_user_when_article_not_found(
    authenticated_ac: AsyncClient,
):
    response = await authenticated_ac.delete(f"/articles/delete/slddldldld")
    assert response.status_code == 404