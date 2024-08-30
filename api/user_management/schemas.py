from pydantic import BaseModel

from api.token.schemas import Token


class UserBase(BaseModel):
    name: str
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int

    class Config:
        orm_mode = True


class Login(BaseModel):
    email: str
    password: str


class LoginResponse(User):
    token_info: Token
