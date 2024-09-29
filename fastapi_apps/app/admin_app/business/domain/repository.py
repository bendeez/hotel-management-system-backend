from app.admin_app.business_user.domain.repository import BusinessUserRepository
from app.admin_app.business.domain.models import Business


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
