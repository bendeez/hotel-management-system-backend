from fastapi import Depends
from app.business.service import BusinessService
from app.user.service import UserService
from app.tools.db.database_transaction import DatabaseTransactionService
from app.accounts.models import Accounts
from app.accounts.enums import AccountType
from app.user.schemas import UserAccountCreate
from app.business.schemas import BusinessAccountCreate
from app.accounts.exceptions import BusinessForbidden


class AccountsService(BusinessService, UserService):

    def __init__(self, transaction: DatabaseTransactionService = Depends(DatabaseTransactionService)):
        super().__init__(transaction=transaction)

    async def create_base_account(self, account_type: AccountType):
        account = await self.transaction.create(model=Accounts, type=account_type.value)
        return account

    async def create_user_account(self, user: UserAccountCreate):
        account = await self.create_base_account(account_type=AccountType.USER)
        user_account = await self.create_user(user=user, account_id=account.id)
        return user_account

    async def create_business_account(self, business: BusinessAccountCreate):
        account = await self.create_base_account(account_type=AccountType.BUSINESS)
        business_account = await self.create_business(business=business, account_id=account.id)
        return business_account

    async def create_business_user_account(self, business, business_user: BusinessAccountCreate):
        if business.id != business_user.id:
            raise BusinessForbidden()
        account = await self.create_base_account(account_type=AccountType.BUSINESS)
        business_user_account = await self.create_user(user=business_user, account_id=account.id)
        return business_user_account