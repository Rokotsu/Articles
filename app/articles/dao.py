from typing import Optional

from app.dao.base import BaseDAO
from sqlalchemy import insert
from app.articles.models import Articles
from app.database import async_session_maker
from app.exceptions import ArticleCannotBeAddException
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
        date_publication: Optional[datetime] = None
    ):
        if date_publication is None:
            date_publication = datetime.now()
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