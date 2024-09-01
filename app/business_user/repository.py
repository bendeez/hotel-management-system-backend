from app.tools.base_repository import BaseRepository
from app.business_user.models import Business_Users


class BusinessUserRepository(BaseRepository):
    async def get_business_user_by_email(self, email: str):
        business_user = await self._get_one(
            model=Business_Users, filters=[Business_Users.email == email]
        )
        return business_user

    async def get_business_user_by_id(self, business_id: int, business_user_id: int):
        business_user = await self._get_one(
            model=Business_Users,
            filters=[
                Business_Users.id == business_user_id,
                Business_Users.business_id == business_id,
            ],
        )
        return business_user
