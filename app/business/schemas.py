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


class BusinessUserAccountBase(BaseModel):
    email: str
    business_id: int
    role_name: str


class BusinessUserAccountOut(BusinessUserAccountBase):
    id: int


class BusinessUserAccountCreate(BusinessUserAccountBase):
    password: str


class BusinessUserAccountIn(BaseModel):
    email: str
    password: str
