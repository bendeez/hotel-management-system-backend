from pydantic import BaseModel, EmailStr
from typing import Literal


class BusinessAccountCreate(BaseModel):
    account_type: Literal["business"]
    email: EmailStr
    name: str
    location: str
