from fastapi import Depends
from app.business.service import BusinessService
from app.user.service import UserService
from app.tools.db.database_transaction import DatabaseTransactionService
from app.accounts.exceptions import BusinessForbidden, NotABusiness
from app.accounts.schemas import BusinessUserAccountCreate, AccountCreate
from app.accounts.models import Business_Users
from app.accounts.schemas import Account
from app.accounts.exceptions import BusinessUserUsernameAlreadyExists


class AccountsService(BusinessService, UserService):
    def __init__(
        self,
        transaction: DatabaseTransactionService = Depends(DatabaseTransactionService),
    ):
        super().__init__(transaction=transaction)

    async def create_business_user_account(
        self, account: Account, business_user: BusinessUserAccountCreate
    ):
        if account.type != "business":
            raise NotABusiness()
        if account.id != business_user.business_id:
            raise BusinessForbidden()
        existing_business_user = await self.get_business_user_by_username(
            username=business_user.username
        )
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

    async def create_account(self, account: AccountCreate):
        if account.type == "users":
            account = await self.create_user_account(user=account)
        elif account.type == "business":
            account = await self.create_business_account(business=account)
        else:
            raise ValueError("invalid account type")
        return account
