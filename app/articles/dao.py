from typing import Optional

from app.dao.base import BaseDAO
from sqlalchemy import insert, delete, update, select
from app.articles.models import Articles
from app.database import async_session_maker
from app.exceptions import ArticleCannotBeAddException, ArticleCannotBeEditException, CannotFindAuthorException, \
    CannotFindDateException
from datetime import datetime

#Для взаимодействия статьи с БД.
class ArticleDAO(BaseDAO):
    model = Articles

    @classmethod
    async def add_article(cls, article_data: dict):
        try:
            async with async_session_maker() as session:
                query = insert(cls.model).values(**article_data)
                result = await session.execute(query)
                await session.commit()
                return result
        except ArticleCannotBeAddException:
            raise ArticleCannotBeAddException

    @classmethod
    async def delete(cls, **filter_by):
        async with async_session_maker() as session:
            query = delete(cls.model).filter_by(**filter_by)
            await session.execute(query)
            await session.commit()

    @classmethod
    async def put_article(cls, article_title: str, article_data: dict):
        try:
            async with async_session_maker() as session:
                query = (update(cls.model).where(cls.model.title == article_title).values(**article_data))
                result = await session.execute(query)
                await session.commit()
                return result
        except ArticleCannotBeEditException:
            raise ArticleCannotBeEditException

    @classmethod
    async def find_by_username(cls, **filter_by: str):
        try:
            async with async_session_maker() as session:
                query = select(cls.model).where(cls.model.author == filter_by['author'])
                result = await session.execute(query)
                return result.scalars().all()
        except CannotFindAuthorException:
            raise CannotFindAuthorException

    @classmethod
    async def find_by_date(cls, datee: datetime) -> int:
        try:
            async with async_session_maker() as session:
                query = select(cls.model).where(cls.model.date_publication == datee)
                result = await session.execute(query)
                return result.mappings().all()
        except CannotFindDateException:
            raise CannotFindDateException
