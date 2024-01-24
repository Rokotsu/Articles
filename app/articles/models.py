from sqlalchemy import Column, Date, ForeignKey, String
from sqlalchemy.orm import relationship

from app.database import Base


class Articles(Base):
    __tablename__ = "articles"

    title = Column(String, primary_key=True, nullable=False)
    content = Column(String, nullable=False)
    date_publication = Column(Date, nullable=False)
    author = Column(ForeignKey("users.username"))

    author_username = relationship("Users", back_populates="articles")