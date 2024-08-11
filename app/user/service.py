from app.tools.base_service import BaseService
from app.user.models import Users
from app.user.schemas import UserCreate


class UserService(BaseService):
    async def get_user_by_id(self, user_id: int):
        user = await self.transaction.get_one(model=Users, filter={Users.id: user_id})
        return user

    async def get_user_by_email(self, email: str):
        user = await self.transaction.get_one(model=Users, filter={Users.email: email})
        return user

    async def create_user_account(self, user: UserCreate):
        new_user = await self.transaction.create(
            model=Users,
            email=user.email,
            password=user.password,
            role=user.role.value,
        )
        return new_user

    async def delete_user_account(self, user_instance: Users):
        await self.transaction.delete(model_instance=user_instance)
