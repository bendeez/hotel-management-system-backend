from app.accounts.models import Accounts
from app.tools.base_repository import BaseRepository


class AccountsRepository(BaseRepository):
    async def get_account_by_email(self, email: str, load_sub=False):
        relationships = []
        if load_sub:
            relationships.append(Accounts.sub)
        account = await self.get_one(
            model=Accounts, relationships=relationships, filter={Accounts.email: email}
        )
        return account

    async def get_account_by_id(self, account_id: int, load_sub=False):
        relationships = []
        if load_sub:
            relationships.append(Accounts.sub)
        account = await self.get_one(
            model=Accounts,
            relationships=relationships,
            filter={Accounts.id: account_id},
        )
        return account.sub
