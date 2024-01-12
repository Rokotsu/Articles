from pydantic import BaseModel
from datetime import date


class SAtricles(BaseModel):
    title: str
    content: str
    date_publication: date
    author: str

class SNewArticle(BaseModel):
    title: str
    content: str