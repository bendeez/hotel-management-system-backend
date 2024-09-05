from admin.app.business_user.repository import BusinessUserRepository
from admin.app.business.models import Business


class BusinessRepository(BusinessUserRepository):
    async def get_business_by_email(self, email: str):
        business = await self._get_one(
            model=Business, filters=[Business.email == email]
        )
        return business

    async def get_business_by_id(self, business_id: int):
        business = await self._get_one(
            model=Business, filters=[Business.id == business_id]
        )
        return business
