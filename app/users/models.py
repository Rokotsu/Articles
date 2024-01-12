from sqlalchemy import Column, String

from app.database import Base


class Users(Base):
    __tablename__ = "users"

    username = Column(String, primary_key=True, nullable=False)
    email = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, nullable=False)