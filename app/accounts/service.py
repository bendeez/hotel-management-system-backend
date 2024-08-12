from fastapi import Depends
from app.business.service import BusinessService
from app.user.service import UserService
from app.tools.db.database_transaction import DatabaseTransactionService
from app.accounts.exceptions import BusinessForbidden
from app.accounts.schemas import BusinessUserAccountCreate
from app.accounts.models import Business_Users
from app.business.models import Business
from app.accounts.exceptions import BusinessUserUsernameAlreadyExists


class AccountsService(BusinessService, UserService):
    def __init__(
        self,
        transaction: DatabaseTransactionService = Depends(DatabaseTransactionService),
    ):
        super().__init__(transaction=transaction)

    async def create_business_user_account(
        self, business: Business, business_user: BusinessUserAccountCreate
    ):
        if business.id != business_user.business_id:
            raise BusinessForbidden()
        existing_business_user = await self.get_business_user_by_username(username=business_user.username)
        if existing_business_user is not None:
            raise BusinessUserUsernameAlreadyExists()
        business_user.password = self.hash_service.hash(business_user.password)
        business_user = await self.transaction.create(
            model=Business_Users, **business_user.model_dump()
        )
        return business_user

    async def get_business_user_by_username(self, username: str):
        business_user = await self.transaction.get_one(
            model=Business_Users, filter={Business_Users.username: username}
        )
        return business_user

    async def get_business_user_by_id(self, business_user_id: int):
        business_user = await self.transaction.get_one(
            model=Business_Users, filter={Business_Users.id: business_user_id}
        )
        return business_user
