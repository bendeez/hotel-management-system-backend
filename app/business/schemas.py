from pydantic import BaseModel, EmailStr
from typing import Literal


class BusinessAccountIn(BaseModel):
    type: Literal["business"] = "business"
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
