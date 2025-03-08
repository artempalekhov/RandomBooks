from typing import Annotated
from sqlalchemy.orm import Mapped, mapped_column
from app.config import Base

intpk = Annotated[int, mapped_column(primary_key=True, autoincrement=True)]


class BookModel(Base):
    __tablename__ = "Books"

    id: Mapped[intpk]
    title: Mapped[str]
    author: Mapped[str]
    genre: Mapped[str]
    description: Mapped[str]
    imgLink: Mapped[str]