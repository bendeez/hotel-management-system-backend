from pydantic import BaseModel, EmailStr


class BusinessAccountCreate(BaseModel):
    email: EmailStr
    master_password: str
    name: str
    location: str

class BusinessAccountOut(BaseModel):
    id: int
    email: EmailStr
    name: str
    location: str