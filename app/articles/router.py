from datetime import datetime

from fastapi import APIRouter, Depends
# from pydantic import TypeAdapter, model_validator

from app.articles.schemas import SArticles, SNewArticles
from app.users.dependencies import get_current_user
from app.users.models import Users
from app.articles.dao import AtricleDAO
from app.exceptions import TitleAlreadyExistsException

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
    writing = await AtricleDAO.add_article(
        title=article.title,
        content=article.content,
        author=user.username
    )
    if not article:
        raise TitleAlreadyExistsException
    return "all_good"

@router_articles.delete("/{title_name}")
async def remove_article(
    title_name: str,
    current_user: Users = Depends(get_current_user),
):
    await AtricleDAO.delete(title=title_name, author=current_user.username)

