from sqlalchemy import insert

from app.articles.models import Articles
from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.exceptions import ArticleCannotBeAddException
from app.users.models import Users
from datetime import datetime



class UserDAO(BaseDAO):
    model = Users

    @classmethod
    async def add_article(
        cls,
        title: str,
        content: str,
        date_publication: datetime.now(),
        author: str
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


