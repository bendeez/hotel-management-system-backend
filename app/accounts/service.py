from app.tools.base_service import BaseService
from app.accounts.schemas import AccountCreate
from app.accounts.enums import AccountMapper
from app.accounts.models import Accounts


class AccountsService(BaseService):

    async def create_account(self, account: AccountCreate):
        specific_account = getattr(AccountMapper, account.account_type)
        account_rel_attr = f"{account.account_type}_accounts"
        account = await self.transaction.create(model=Accounts,
                              relationship={account_rel_attr:specific_account},
                              account_type=account.account_type)
        return account
