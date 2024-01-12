from fastapi import APIRouter, Depends

from app.articles.schemas import SAtricles
from app.users.dependencies import get_current_user
from app.users.models import Users
from app.articles.dao import AtricleDAO

router = APIRouter(
    prefix="/articles",
    tags=["Статьи"],
)

@router.get("")
async def get_articles(user: Users = Depends(get_current_user)) -> list[SAtricles]:
    return await AtricleDAO.find_all()

