from pydantic import BaseModel


class BusinessUserAccountBase(BaseModel):
    email: str
    role_name: str


class BusinessUserAccountOut(BusinessUserAccountBase):
    id: int


class BusinessUserAccountCreate(BusinessUserAccountBase):
    password: str


class BusinessUserAccountIn(BaseModel):
    email: str
    password: str


class BusinessUserAccountDelete(BaseModel):
    business_user_id: int
