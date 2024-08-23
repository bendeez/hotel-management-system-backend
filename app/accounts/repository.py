from app.accounts.models import Accounts
from app.tools.base_repository import BaseRepository
from sqlalchemy import or_
from app.user.models import Users
from app.business.models import Business, Business_Users


class AccountsRepository(BaseRepository):
    async def get_account_by_email(self, email: str):
        stmt = self._build_query(model=Accounts, polymorphic=True)
        stmt = stmt.where(
            or_(
                Users.email == email,
                Business.email == email,
                Business_Users.email == email,
            )
        )
        account = await self.db.execute(stmt)
        return account.scalars().first()

    async def get_account_by_id(self, account_id: int):
        account = await self._get_one(
            model=Accounts,
            polymorphic=True,
            filter={Accounts.id: account_id},
        )
        return account
