from pydantic import BaseModel, EmailStr
from typing import Literal
from app.accounts.enums import AccountType


class UserAccountIn(BaseModel):
    type: Literal[AccountType.USERS] = AccountType.USERS
    email: EmailStr
    password: str


class UserAccountCreate(UserAccountIn):
    pass


class UserAccountOut(BaseModel):
    id: int
    email: EmailStr
