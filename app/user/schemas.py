from pydantic import BaseModel, EmailStr
from typing import Literal
from enum import Enum


class UserAccountIn(BaseModel):
    email: EmailStr
    password: str


class UserRoleEnum(Enum):
    admin = "admin"
    user = "user"


class UserAccountCreate(UserAccountIn):
    account_type: Literal["user"]
    role: UserRoleEnum


class UserAccountOut(BaseModel):
    id: int
    email: EmailStr
    role: UserRoleEnum
