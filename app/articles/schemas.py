from datetime import date

from pydantic import BaseModel


class SArticles(BaseModel):
    title: str
    content: str
    date_publication: date
    author: str

    class Config:
        from_attributes = True


class SNewArticles(BaseModel):
    title: str
    content: str


