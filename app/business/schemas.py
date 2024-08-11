from pydantic import BaseModel, EmailStr


class BusinessAccountCreate(BaseModel):
    email: EmailStr
    name: str
    location: str
