from app.tools.base_service import BaseService
from app.user.models import Users


class UserService(BaseService):
    async def get_user_by_id(self, user_id: int):
        user = await self.transaction.get_one(model=Users, filter={Users.id: user_id})
        return user

    async def get_user_by_email(self, email: str):
        user = await self.transaction.get_one(model=Users, filter={Users.email: email})
        return user