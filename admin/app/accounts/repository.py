from admin.app.accounts.models import Accounts
from admin.app.tools.base_repository import BaseRepository
from admin.app.user.models import Users
from admin.app.business.models import Business
from admin.app.business_user.models import Business_Users
from sqlalchemy import or_


class AccountsRepository(BaseRepository):
    async def get_account_by_email(self, email: str):
        account = await self._get_one(
            model=Accounts,
            polymorphic=True,
            filters=[
                or_(
                    Users.email == email,
                    Business.email == email,
                    Business_Users.email == email,
                )
            ],
        )
        return account

    async def get_account_by_id(self, account_id: int):
        account = await self._get_one(
            model=Accounts,
            polymorphic=True,
            filters=[Accounts.id == account_id],
        )
        return account
