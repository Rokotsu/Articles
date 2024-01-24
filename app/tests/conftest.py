import asyncio
import json
from datetime import datetime

import pytest
from httpx import AsyncClient
from sqlalchemy import insert

from app.articles.models import Articles
from app.config import settings
from app.database import Base, async_session_maker, engine
from app.main import app as fastapi_app
from app.users.models import Users


@pytest.fixture(scope="session", autouse=True)
async def prepare_database():
    # Обязательно убеждаемся, что работаем с тестовой БД
    assert settings.MODE == "TEST"

    async with engine.begin() as conn:
        # Удаление всех заданных нами таблиц из БД
        await conn.run_sync(Base.metadata.drop_all)
        # Добавление всех заданных нами таблиц из БД
        await conn.run_sync(Base.metadata.create_all)

    def open_mock_json(model: str):
        with open(f"app/tests/mock_{model}.json", encoding="utf-8") as file:
            return json.load(file)

    users = open_mock_json("users")
    articles = open_mock_json("articles")

    for article in articles:
        article["date_publication"] = datetime.strptime(
            article["date_publication"], "%Y-%m-%d"
        )

    async with async_session_maker() as session:
        for Model, values in [(Users, users), (Articles, articles)]:
            query = insert(Model).values(values)
            await session.execute(query)

        await session.commit()  # чтобы все эти данные оказались в базе


# Взято из документации к pytest-asyncio
# Создаем новый event loop для прогона тестов
@pytest.fixture(scope="session")
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
async def ac():  # AsycnClient
    "Асинхронный клиент для тестирования эндпоинтов"
    async with AsyncClient(app=fastapi_app, base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="session")
async def authenticated_ac():
    "Асинхронный аутентифицированный клиент для тестирования эндпоинтов"
    async with AsyncClient(app=fastapi_app, base_url="http://test") as ac:
        await ac.post(
            "/auth/login",
            json={
                "username": "test",
                "password": "test",
            },
        )
        print(ac.cookies["article_access_token"])
        # assert ac.cookies["article_access_token"]
        yield ac
