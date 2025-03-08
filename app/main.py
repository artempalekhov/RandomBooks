from fastapi import FastAPI, HTTPException, Request, Response
from sqlalchemy import and_, func, select
import uvicorn
from app.books.models import *
from app.database import Endpoints, SessionDep
from fastapi.middleware.cors import CORSMiddleware
from app.books.schemas import *
from app.users.models import *
from app.users.schemas import *
from app.auth import security, config

app = FastAPI()

origins = [
    "http://127.0.0.1:5500"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def get_token_cookie(request: Request):
        token = request.cookies.get("my_access_token")
        if not token:
            raise HTTPException(status_code=401, detail=f"Отсутствует токен")
        return token

async def decode_token(request: Request):
        token = await get_token_cookie(request)
        payload = security._decode_token(token)
        user_id = payload.decode(token, "super_puper_secret_key")
        return user_id.sub


@app.post("/register")
async def register_user(data: UserRegisterSchema, session: SessionDep, response: Response):
        existing_user = await session.execute(
            select(UserModel).where((UserModel.email == data.email) | (UserModel.login == data.login)))
        if existing_user.scalars().first():
            raise HTTPException(status_code=409, detail="Такой пользователь существует")

        new_user = UserModel(
            fio=data.fio,
            email=data.email,
            login=data.login,
            password=data.password,
            role=data.role
        )
        session.add(new_user)
        result = await session.execute(select(UserModel).where(UserModel.login == data.login))
        user = result.scalars().first()
        token = security.create_access_token(uid=str(user.id))
        response.set_cookie(config.JWT_ACCESS_COOKIE_NAME, value=token, httponly=True, secure=True, samesite="none", path="/")
        await session.commit()
        return {"ok": True}

@app.post("/login")
async def login_user(data: UserLoginSchema, session: SessionDep, response: Response):
        query = select(UserModel).where(
            and_(
                UserModel.login == data.login,
                UserModel.password == data.password
            )
        )
        result = await session.execute(query)
        user = result.scalars().first()

        if user is None:
            raise HTTPException(status_code=401, detail="Неправильный логин или пароль")

        token = security.create_access_token(uid=str(user.id))
        response.set_cookie(
            key=config.JWT_ACCESS_COOKIE_NAME,
            value=token,
            httponly=True,
            secure=True,
            samesite="none",
            path="/",
        )
        await session.commit()
        return {"access_token": token}

@app.get("/get_all_users/")
async def get_users(session: SessionDep):
    query = select(UserModel)
    result = await session.execute(query)
    return result.scalars().all()

@app.delete("/user/{user_id}")
async def delete_user(user_id: int, session: SessionDep):
        query = select(UserModel).where(UserModel.id == user_id)
        result = await session.execute(query)
        user = result.scalars().first()
    
        if user is None:
            raise HTTPException(status_code=404, detail="Пользователь не найден")
    
        await session.delete(user)
        await session.commit()
        return {"ok": True}

#region CRUD books
@app.post("/books/")
async def add_book(data: BookAddSchema, session: SessionDep):
        new_book = BookModel(
            title=data.title,
            author=data.author,
            genre=data.genre,
            description=data.description,
            imgLink=data.imgLink
        )
        session.add(new_book)
        await session.commit()
        return {"ok": True}

@app.get("/books/")
async def get_books(self, session: SessionDep):
        query = select(BookModel)
        result = await session.execute(query)
        return result.scalars().all()

@app.put("/books/{book_id}")
async def update_book(book_id: int, data: BookAddSchema, session: SessionDep):
        query = select(BookModel).where(BookModel.id == book_id)
        result = await session.execute(query)
        book = result.scalars().first()
    
        if book is None:
            raise HTTPException(status_code=404, detail="Книга не найдена")
    
        book.title = data.title
        book.author = data.author
        book.genre = data.genre
        book.description = data.description
        book.imgLink = data.imgLink
    
        await session.commit()
        return {"ok": True}

@app.delete("/books/{book_id}")
async def delete_book(self, book_id: int, session: SessionDep):
        query = select(BookModel).where(BookModel.id == book_id)
        result = await session.execute(query)
        book = result.scalars().first()
    
        if book is None:
            raise HTTPException(status_code=404, detail="Книга не найдена")
    
        await session.delete(book)
        await session.commit()
        return {"ok": True}

@app.get("/random_book")
async def get_random_book(genre: str, session: SessionDep):
        query = select(BookModel).where(BookModel.genre == genre).order_by(func.random()).limit(1)
        result = await session.execute(query)
        book = result.scalars().first()
    
        if book is None:
            raise HTTPException(status_code=404, detail="Нет доступных книг")
    
        return book

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0")