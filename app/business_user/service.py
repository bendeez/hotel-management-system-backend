from app.business_user.repository import BusinessUserRepository
from fastapi import Depends
from app.business_user.exceptions import NotABusinessUser
from app.business_user.models import Business_Users
from app.accounts.models import Accounts


class BusinessUserService:
    def __init__(
        self, repository: BusinessUserRepository = Depends(BusinessUserRepository)
    ):
        self.repository = repository

    async def get_business_user_account_info(self, account: Accounts):
        if not isinstance(account, Business_Users):
            raise NotABusinessUser()
        return account