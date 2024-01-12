from app.dao.base import BaseDAO
from app.articles.models import Articles

#Для взаимодействия статьи с БД.
class AtricleDAO(BaseDAO):
    model = Articles

