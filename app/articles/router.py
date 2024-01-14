from datetime import datetime

from fastapi import APIRouter, Depends
# from pydantic import TypeAdapter, model_validator

from app.articles.schemas import SArticles, SNewArticles
from app.users.dependencies import get_current_user
from app.users.models import Users
from app.articles.dao import AtricleDAO
from app.exceptions import TitleAlreadyExistsException, CannotDeleteArticleException, CannotFindArticleException

router_articles = APIRouter(
    prefix="/articles",
    tags=["Статьи"],
)

@router_articles.get("")
async def get_articles(user: Users = Depends(get_current_user)) -> list[SArticles]:
    return await AtricleDAO.find_all()


@router_articles.post("", status_code=201)
async def add_article(
        article: SNewArticles,
        user: Users = Depends(get_current_user),
):
    await AtricleDAO.add_article(
        title=article.title,
        content=article.content,
        author=user.username
    )
    if not article:
        raise TitleAlreadyExistsException
    return "all_good"

@router_articles.put("/{title_name}", status_code=201)
async def edit(
        article_data: SNewArticles,
        title_name: str,
        current_user: Users = Depends(get_current_user)
) -> str:
    existing_article = await AtricleDAO.find_one_or_none(title=title_name)
    if existing_article:
            if (current_user.username == existing_article["author"] or current_user.role == "admin") and article_data:
                await AtricleDAO.put_article(
                article_title=title_name,
                article_data=article_data.dict()
                )
                return "success"
            else:
                return "хУЙНЯ"
    else:
        return "Хуйня x2"


@router_articles.delete("/{title_name}")
async def remove_article(
    title_name: str,
    current_user: Users = Depends(get_current_user),
) -> str:

    existing_article = await AtricleDAO.find_one_or_none(title=title_name)

    if existing_article:
            if (
                    current_user.username == existing_article["author"]
                    or current_user.role == "admin"
            ):
                await AtricleDAO.delete(title=title_name, author=current_user.username)
                return "Success edited"
            else:
                raise CannotDeleteArticleException
    else:
        raise CannotFindArticleException



