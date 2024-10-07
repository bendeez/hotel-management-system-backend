from apps.admin_app.business.domain.models import Business, Accounts
from apps.admin_app.business_user.domain.models import Business_Users
from apps.admin_app.business.domain.schemas import BusinessAccountCreate
from apps.admin_app.business_user.domain.schemas import (
    BusinessUserAccountCreate,
)
from apps.admin_app.utils.domain.service import HashService
from apps.admin_app.business.domain.exceptions import (
    BusinessEmailAlreadyExists,
    NotABusiness,
)
from apps.admin_app.business_user.domain.exceptions import (
    BusinessUserEmailAlreadyExists,
    BusinessUserNotFound,
)
from apps.admin_app.business.domain.repository import BusinessRepository


class BusinessService:
    def __init__(self, repository: BusinessRepository):
        self.hash_service = HashService()
        self._repository = repository

    async def create_business_account(self, business: BusinessAccountCreate):
        existing_business = await self._repository.get_business_by_email(
            email=business.email
        )
        if existing_business is not None:
            raise BusinessEmailAlreadyExists()
        business.password = self.hash_service.hash(business.password)
        business_account = await self._repository.create(
            Business(**business.model_dump())
        )
        return business_account

    async def create_business_user_account(
        self,
        account: Accounts,
        business_user: BusinessUserAccountCreate,
    ):
        if not isinstance(account, Business):
            raise NotABusiness()
        existing_business_user = await self._repository.get_business_user_by_email(
            email=business_user.email
        )
        if existing_business_user is not None:
            raise BusinessUserEmailAlreadyExists()
        business_user.password = self.hash_service.hash(business_user.password)
        business_user_account = await self._repository.create(
            Business_Users(**business_user.model_dump(), business_id=account.id)
        )
        return business_user_account

    async def delete_business_account(self, account: Accounts):
        if not isinstance(account, Business):
            raise NotABusiness()
        await self._repository.delete(model_instance=account)

    async def delete_business_user_account(
        self, business_user_id: int, account: Accounts
    ):
        if not isinstance(account, Business):
            raise NotABusiness()
        business_user = await self._repository.get_business_user_by_id(
            business_user_id=business_user_id, business_id=account.id
        )
        if business_user is None:
            raise BusinessUserNotFound()
        await self._repository.delete(model_instance=business_user)

    async def get_business_account_info(self, account: Accounts):
        if not isinstance(account, Business):
            raise NotABusiness()
        return account
