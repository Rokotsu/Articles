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


@pytest.mark.parametrize("username,email,password,role,status_code",[
    ("roma", "artem@email.com", "artem", "admin", 200),
    ("Rebeca", "emaile@email.com", "test", "user", 200)
])
async def test_login_user(username, email, password, role, status_code, ac: AsyncClient):
    response = await ac.post("/auth/login", json={
        "username": username,
        "email": email,
        "password": password,
        "role": role
    })
    print(response)
    assert response.status_code == status_code