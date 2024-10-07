from app.admin_app.accounts.domain.models import Accounts
from tools.domain.base_repository import BaseRepository
from app.admin_app.user.domain.models import Users
from app.admin_app.business.domain.models import Business
from app.admin_app.business_user.domain.models import Business_Users
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
