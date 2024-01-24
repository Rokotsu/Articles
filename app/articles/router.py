from datetime import datetime

from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache

from app.articles.dao import ArticleDAO
from app.articles.schemas import SArticles, SNewArticles
from app.exceptions import (
    ArticleCannotBeAddException,
    CannotChangeArticleException,
    CannotDeleteArticleException,
    CannotFindArticleException,
    CannotFindAuthorException,
    CannotFindDateException,
    TitleAlreadyExistsException,
)
from app.users.dependencies import get_current_user
from app.users.models import Users

router_articles = APIRouter(
    prefix="/articles",
    tags=["Статьи"],
)


# Получение всех статей
@router_articles.get("/all")
@cache(expire=30)
async def get_articles() -> list[SArticles]:
    """
    Получение всех статьей, без регистрации.

    Returns:  \n
        list[SArticles]: Список из всех статей  \n
    """
    return await ArticleDAO.find_all()


@router_articles.get("/author/{by_name}")
@cache(expire=30)
async def get_article_by_author(user) -> list[SArticles]:
    """
    Получение всех статьей по автору, без регистрации.

    Returns: \n
        list[SArticles]: Список из всех статей по автору \n
    """
    try:
        return await ArticleDAO.find_by_username(author=user)
    except:
        raise CannotFindAuthorException


@router_articles.get("/date/{by_date}")
@cache(expire=30)
async def get_article_by_date(date: datetime) -> list[SArticles]:
    """
    Получение всех статьей по автору, без регистрации.

    Returns: \n
        list[SArticles]: Список из всех статей по дате публикации \n
    """
    try:
        return await ArticleDAO.find_by_date(datee=date)
    except:
        raise CannotFindDateException


# создание статьи, с проверкой на атентификацию
@router_articles.post("/create", status_code=201)
async def add_article(
    article: SNewArticles,
    user: Users = Depends(get_current_user),
):
    """
    Add a new article.

    Args: \n
        article (SNewArticles): The new article to add (title and content). \n
        user (Users): The user who added the article and authentication check. \n

    Raises: \n
        TitleAlreadyExistsException: If the article title already exists. \n

    Returns: \n
        str: "all_good" if the article was successfully added. \n
    """
    try:
        article_data = {
            "title": article.title,
            "content": article.content,
            "author": user.username,
            "date_publication": datetime.now().date(),
        }
        existing_article = await ArticleDAO.find_one_or_none(title=article.title)
        if existing_article:
            raise TitleAlreadyExistsException
        else:
            await ArticleDAO.add_article(article_data)
            return "all_good"
    except ArticleCannotBeAddException:
        raise TitleAlreadyExistsException


# редактирование статьи, с проверкой на атентификацию и роль
@router_articles.put("/update/{title_name}", status_code=201)
async def edit(
    article_data: SNewArticles,
    title_name: str,
    current_user: Users = Depends(get_current_user),
) -> str:
    """
    Edit an article.

    Args: \n
        article_data (SNewArticles): Новые данные для статьи. \n
        title_name (str): Поиск статьи по заголовку \n
        current_user (Users): проверка на аутентификацию \n

    :Raises: \n
        CannotChangeArticleException: Если статья не может быть изменена \n
        CannotFindArticleException: Если не удаётся найти статью \n

    Returns: \n
        str: "success" если статья изменена успешно. \n
    """
    existing_article = await ArticleDAO.find_one_or_none(title=title_name)
    if existing_article:
        if (
            current_user.username == existing_article["author"]
            or current_user.role == "admin"
        ) and article_data:
            await ArticleDAO.put_article(
                article_title=title_name, article_data=article_data.dict()
            )
            return "success"
        else:
            raise CannotChangeArticleException
    else:
        raise CannotFindArticleException


# удаление статьи, с проверкой на атентификацию и роль
@router_articles.delete("/delete/{title_name}")
async def remove_article(
    title_name: str,
    current_user: Users = Depends(get_current_user),
) -> str:
    """
    Удаление статьи.

    Args: \n
        title_name (str): Поиск статьи для удаления, по заголовку. \n
        current_user (Users): проверка на аутентификацию. \n

    Raises: \n
        CannotDeleteArticleException: Если пользователь не автор статьи и не админ. \n
        CannotFindArticleException: Если статьи не существует. \n

    Returns: \n
        str: "Success edited" если статья была успешно удалена. \n
    """

    existing_article = await ArticleDAO.find_one_or_none(title=title_name)

    if existing_article:
        if (
            current_user.username == existing_article["author"]
            or current_user.role == "admin"
        ):
            await ArticleDAO.delete(title=title_name, author=current_user.username)
            return "Success edited"
        else:
            raise CannotDeleteArticleException
    else:
        raise CannotFindArticleException
