from typing import Annotated
from sqlalchemy.orm import Mapped, mapped_column
from app.config import Base

intpk = Annotated[int, mapped_column(primary_key=True, autoincrement=True)]

class UserModel(Base):
    __tablename__ = "Users"

    id: Mapped[intpk]
    fio: Mapped[str]
    email: Mapped[str]
    login: Mapped[str]
    password: Mapped[str]
    role: Mapped[str]

