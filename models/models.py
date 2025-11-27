from pydantic import BaseModel


class UserBase(BaseModel):
    name: str
    lastname: str
    email: str


class UserCreate(UserBase):
    password: str


class EmailUser(BaseModel):
    email: str


class CodeUser(EmailUser):
    code: str

class EmailPasswordLogin(BaseModel):
    email: str
    password: str


class UserPassword(BaseModel):
    password: str