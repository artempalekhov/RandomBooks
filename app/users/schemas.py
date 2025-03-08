from pydantic import BaseModel

class UserRegisterSchema(BaseModel):
    fio: str
    email: str
    login: str
    password: str
    role: str = "User"

class UserLoginSchema(BaseModel):
    login: str
    password: str