from pydantic import BaseModel, EmailStr


class UserAccountIn(BaseModel):
    email: EmailStr
    password: str


class UserAccountCreate(UserAccountIn):
    role_id: int


class UserAccountOut(BaseModel):
    id: int
    email: EmailStr
    role_id: int
