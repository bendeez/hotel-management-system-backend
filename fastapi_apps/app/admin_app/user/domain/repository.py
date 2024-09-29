from app.tools.domain.base_repository import BaseRepository
from app.admin_app.user.domain.models import Users


class UserRepository(BaseRepository):
    async def get_user_by_id(self, user_id: int):
        user = await self._get_one(model=Users, filters=[Users.id == user_id])
        return user

    async def get_user_by_email(self, email: str):
        user = await self._get_one(model=Users, filters=[Users.email == email])
        return user
