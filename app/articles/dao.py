from typing import Optional

from app.dao.base import BaseDAO
from sqlalchemy import insert, delete, update
from app.articles.models import Articles
from app.database import async_session_maker
from app.exceptions import ArticleCannotBeAddException, ArticleCannotBeEditException
from datetime import datetime

#Для взаимодействия статьи с БД.
class AtricleDAO(BaseDAO):
    model = Articles

    @classmethod
    async def add_article(
        cls,
        title: str,
        content: str,
        author: str,
        date_publication=datetime.now().date()
    ):
        try:
            async with async_session_maker() as session:
                add_article = (
                    insert(Articles)
                    .values(
                        title=title,
                        content=content,
                        date_publication=date_publication,
                        author=author
                    )
                    .returning(
                        Articles.title,
                        Articles.content,
                        Articles.date_publication,
                        Articles.author
                    )
                )
                new_article = await session.execute(add_article)
                await session.commit()
                return new_article.mappings().one()
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
