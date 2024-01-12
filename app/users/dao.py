from app.dao.base import BaseDAO
from app.users.models import Users


#Для взаимодействия юзера с БД.
class UserDAO(BaseDAO):
    model = Users