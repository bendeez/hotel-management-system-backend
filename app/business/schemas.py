from pydantic import BaseModel, EmailStr


class BusinessAccountIn(BaseModel):
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
