from app.admin_app.business_user.domain.repository import BusinessUserRepository
from app.admin_app.business_user.domain.exceptions import NotABusinessUser
from app.admin_app.business_user.domain.models import Business_Users
from app.admin_app.accounts.domain.models import Accounts


class BusinessUserService:
    def __init__(self, repository: BusinessUserRepository):
        self._repository = repository

    async def get_business_user_account_info(self, account: Accounts):
        if not isinstance(account, Business_Users):
            raise NotABusinessUser()
        return account
