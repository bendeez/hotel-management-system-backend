from app.user.schemas import UserAccountCreate


class BusinessUserAccountCreate(UserAccountCreate):
    business_id: int # not optional



