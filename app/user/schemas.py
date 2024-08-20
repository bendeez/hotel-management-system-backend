from pydantic import BaseModel, EmailStr


class UserAccountIn(BaseModel):
    email: EmailStr
    password: str


class UserAccountCreate(UserAccountIn):
    pass


class UserAccountOut(BaseModel):
    id: int
    email: EmailStr
