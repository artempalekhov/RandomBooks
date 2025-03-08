from typing import Optional
from pydantic import BaseModel

class BookAddSchema(BaseModel):
    title: str
    author: str
    genre: str
    description: str
    imgLink: str

class BookSchema(BookAddSchema):
    id: int