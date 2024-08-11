from pydantic import BaseModel, EmailStr
from enum import Enum


class UserAccountIn(BaseModel):
    email: EmailStr
    password: str


class UserRoleEnum(Enum):
    admin = "admin"
    user = "user"


class UserAccountCreate(UserIn):
    role: UserRoleEnum


class UserAccountOut(BaseModel):
    id: int
    email: EmailStr
    role: UserRoleEnum
