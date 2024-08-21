from app.tools.base_repository import BaseRepository
from app.user.models import Users


class UserRepository(BaseRepository):
    async def get_user_by_id(self, user_id: int):
        user = await self.get_one(model=Users, filter={Users.id: user_id})
        return user

    async def get_user_by_email(self, email: str):
        user = await self.get_one(model=Users, filter={Users.email: email})
        return user