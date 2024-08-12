from app.user.schemas import UserAccountCreate, UserAccountIn, UserAccountOut
from app.business.schemas import BusinessAccountCreate, BusinessAccountIn, BusinessAccountOut
from pydantic import BaseModel

class BusinessUserAccountOut(BaseModel):
    username: str

class BusinessUserAccountIn(BaseModel):
    username: str
    password: str


class BusinessUserAccountCreate(BusinessUserAccountIn):
    business_id: int

