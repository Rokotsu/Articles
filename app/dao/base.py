from sqlalchemy import delete, insert, select


from app.database import async_session_maker



class BaseDAO:
    model = None

    @classmethod
    async def find_by_title(cls, title: str):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(str=title)
            result = await session.execute(query)
            return result.mappings().one_or_none()

    @classmethod
    async def find_one_or_none(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(**filter_by)
            result = await session.execute(query)
            return result.mappings().one_or_none()

    @classmethod
    async def find_all(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(**filter_by)
            result = await session.execute(query)
            return result.mappings().all()