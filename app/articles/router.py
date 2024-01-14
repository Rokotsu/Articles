

from fastapi import APIRouter, Depends


from app.articles.schemas import SArticles, SNewArticles
from app.users.dependencies import get_current_user
from app.users.models import Users
from app.articles.dao import AtricleDAO
from app.exceptions import TitleAlreadyExistsException, CannotDeleteArticleException, CannotFindArticleException, CannotChangeArticleException

router_articles = APIRouter(
    prefix="/articles",
    tags=["Статьи"],
)
#Получение всех статей
@router_articles.get("")
async def get_articles() -> list[SArticles]:
    """
        Получение всех статьей, без регистрации.

        Returns:  \n
            list[SArticles]: Список из всех статей  \n
    """
    return await AtricleDAO.find_all()

#создание статьи, с проверкой на атентификацию
@router_articles.post("", status_code=201)
async def add_article(
        article: SNewArticles,
        user: Users = Depends(get_current_user),
):
    """
        Добавление новой статьи.

        Args: \n
            article (SNewArticles): добавление статьи(заголовк и контент). \n
            user (Users): Пользователь, который добавил статью а так же проверка на аутентификацию. \n

        Raises: \n
            TitleAlreadyExistsException: Если заголовок для статьи уже существует. \n

        Returns: \n
            str: "all_good" Если статья была успешно добавлена.\n
    """
    await AtricleDAO.add_article(
        title=article.title,
        content=article.content,
        author=user.username
    )
    if not article:
        raise TitleAlreadyExistsException
    return "all_good"

#редактирование статьи, с проверкой на атентификацию и роль
@router_articles.put("/{title_name}", status_code=201)
async def edit(
        article_data: SNewArticles,
        title_name: str,
        current_user: Users = Depends(get_current_user)
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
    existing_article = await AtricleDAO.find_one_or_none(title=title_name)
    if existing_article:
            if (current_user.username == existing_article["author"] or current_user.role == "admin") and article_data:
                await AtricleDAO.put_article(
                article_title=title_name,
                article_data=article_data.dict()
                )
                return "success"
            else:
                raise CannotChangeArticleException
    else:
        raise CannotFindArticleException

#удаление статьи, с проверкой на атентификацию и роль
@router_articles.delete("/{title_name}")
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



