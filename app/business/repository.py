from app.tools.base_repository import BaseRepository
from app.business.models import Business, Business_Users


class BusinessRepository(BaseRepository):
    async def get_business_by_email(self, email: str):
        business = await self.get_one(model=Business, filter={Business.email: email})
        return business

    async def get_business_by_id(self, business_id: int):
        business = await self.get_one(model=Business, filter={Business.id: business_id})
        return business

    async def get_business_user_by_email(self, email: str):
        business_user = await self.transaction.get_one(
            model=Business_Users, filter={Business_Users.username: email}
        )
        return business_user

    async def get_business_user_by_id(self, business_user_id: int):
        business_user = await self.transaction.get_one(
            model=Business_Users, filter={Business_Users.id: business_user_id}
        )
        return business_user