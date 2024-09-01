from app.accounts.models import Accounts
from app.tools.base_repository import BaseRepository
from app.user.models import Users
from app.business.models import Business
from app.business_user.models import Business_Users
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
