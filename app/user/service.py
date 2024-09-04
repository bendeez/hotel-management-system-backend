from fastapi import Depends
from app.user.schemas import UserAccountCreate
from app.utils.service import HashService
from app.user.exceptions import UserEmailAlreadyExists, NotAUser
from app.user.models import Users
from app.user.repository import UserRepository
from app.accounts.models import Accounts


class UserService:
    def __init__(self, repository: UserRepository = Depends(UserRepository)):
        self.hash_service = HashService()
        self._repository = repository

    async def create_user_account(self, user: UserAccountCreate):
        existing_user = await self._repository.get_user_by_email(email=user.email)
        if existing_user is not None:
            raise UserEmailAlreadyExists()
        user.password = self.hash_service.hash(user.password)
        user_account = await self._repository.create(Users(**user.model_dump()))
        return user_account

    async def delete_user_account(self, account: Accounts):
        await self._repository.delete(model_instance=account)

    async def get_user_account_info(self, account: Accounts):
        if not isinstance(account, Users):
            raise NotAUser()
        return account
