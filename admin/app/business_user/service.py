from admin.app.business_user.repository import BusinessUserRepository
from fastapi import Depends
from admin.app.business_user.exceptions import NotABusinessUser
from admin.app.business_user.models import Business_Users
from admin.app.accounts.models import Accounts


class BusinessUserService:
    def __init__(
        self, repository: BusinessUserRepository = Depends(BusinessUserRepository)
    ):
        self._repository = repository

    async def get_business_user_account_info(self, account: Accounts):
        if not isinstance(account, Business_Users):
            raise NotABusinessUser()
        return account
