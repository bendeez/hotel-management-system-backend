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


class BusinessUserAccountOut(BaseModel):
    email: str
    business_id: int
    role_name: str


class BusinessUserAccountCreate(BusinessUserAccountOut):
    password: str


class BusinessUserAccountIn(BaseModel):
    email: str
    password: str
