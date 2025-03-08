from pydantic_settings import BaseSettings
from sqlalchemy.orm import DeclarativeBase

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite+aiosqlite:///./books.db"

settings = Settings()

class Base(DeclarativeBase):
    pass