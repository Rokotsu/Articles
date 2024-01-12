from app.dao.base import BaseDAO
from app.users.models import Users



class UserDAO(BaseDAO):
    model = Users
    #
    # @classmethod
    # async def add_article(
    #         cls,
    #         title: str,
    #         content: str,
    #         date_publication: date
    #
    # ):

