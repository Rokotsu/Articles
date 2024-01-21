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