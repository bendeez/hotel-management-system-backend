from fastapi import Depends
from app.tools.base_service import BaseService
from app.user.models import Users
from app.user.schemas import UserAccountCreate
from app.utils.service import HashService
from app.tools.db.database_transaction import DatabaseTransactionService
from app.user.exceptions import UserEmailAlreadyExists


class UserService(BaseService):
    def __init__(
        self,
        transaction: DatabaseTransactionService = Depends(DatabaseTransactionService),
    ):
        super().__init__(transaction=transaction)
        self.hash_service = HashService()

    async def get_user_by_id(self, user_id: int):
        user = await self.transaction.get_one(model=Users, filter={Users.id: user_id})
        return user

    async def get_user_by_email(self, email: str):
        user = await self.transaction.get_one(model=Users, filter={Users.email: email})
        return user

    async def create_user_account(self, user: UserAccountCreate):
        existing_user = await self.get_user_by_email(email=user.email)
        if existing_user is not None:
            raise UserEmailAlreadyExists()
        user.password = self.hash_service.hash(user.password)
        user_account = await self.transaction.create(
            model=Users, **user.model_dump()
        )
        return user_account
