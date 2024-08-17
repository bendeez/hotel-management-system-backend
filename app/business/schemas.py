from pydantic import BaseModel, EmailStr
from typing import Literal
from app.accounts.enums import AccountType


class BusinessAccountIn(BaseModel):
    type: Literal[AccountType.BUSINESS] = AccountType.BUSINESS
    email: EmailStr
    password: str


class BusinessAccountCreate(BusinessAccountIn):
    name: str
    location: str


class BusinessAccountOut(BaseModel):
    id: int
    email: EmailStr
    name: str
    location: str
