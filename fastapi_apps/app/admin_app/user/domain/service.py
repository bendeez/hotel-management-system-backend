from app.admin_app.user.domain.schemas import UserAccountCreate
from app.admin_app.utils.domain.service import HashService
from app.admin_app.user.domain.exceptions import UserEmailAlreadyExists, NotAUser
from app.admin_app.user.domain.models import Users
from app.admin_app.user.domain.repository import UserRepository
from app.admin_app.accounts.domain.models import Accounts


class UserService:
    def __init__(self, repository: UserRepository):
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
