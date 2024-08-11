from pydantic import BaseModel, EmailStr
from enum import Enum


class UserIn(BaseModel):
    email: EmailStr
    password: str


class UserRoleEnum(Enum):
    admin = "admin"
    user = "user"


class UserCreate(UserIn):
    role: UserRoleEnum


class UserOut(BaseModel):
    id: int
    email: EmailStr
    role: UserRoleEnum
