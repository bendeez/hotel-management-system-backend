from pydantic import BaseModel, EmailStr
from typing import Literal


class UserAccountIn(BaseModel):
    type: Literal["users"] = "users"
    email: EmailStr
    password: str


class UserAccountCreate(UserAccountIn):
    pass


class UserAccountOut(BaseModel):
    id: int
    email: EmailStr
