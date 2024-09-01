from app.business.models import Business, Accounts
from app.business_user.models import Business_Users
from app.business.schemas import BusinessAccountCreate
from app.business_user.schemas import (
    BusinessUserAccountCreate,
    BusinessUserAccountDelete,
)
from app.utils.service import HashService
from app.business.exceptions import (
    BusinessEmailAlreadyExists,
    NotABusiness,
    BusinessForbidden,
)
from app.business_user.exceptions import (
    BusinessUserEmailAlreadyExists,
    BusinessUserNotFound,
)
from app.business.repository import BusinessRepository
from fastapi import Depends


class BusinessService:
    def __init__(self, repository: BusinessRepository = Depends(BusinessRepository)):
        self.hash_service = HashService()
        self.repository = repository

    async def create_business_account(self, business: BusinessAccountCreate):
        existing_business = await self.repository.get_business_by_email(
            email=business.email
        )
        if existing_business is not None:
            raise BusinessEmailAlreadyExists()
        business.password = self.hash_service.hash(business.password)
        business_account = await self.repository.create(
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
        existing_business_user = await self.repository.get_business_user_by_email(
            email=business_user.email
        )
        if existing_business_user is not None:
            raise BusinessUserEmailAlreadyExists()
        business_user.password = self.hash_service.hash(business_user.password)
        business_user_account = await self.repository.create(
            Business_Users(**business_user.model_dump(), business_id=account.id)
        )
        return business_user_account

    async def delete_business_account(self, account: Accounts):
        if not isinstance(account, Business):
            raise NotABusiness()
        await self.repository.delete(model_instance=account)

    async def delete_business_user_account(
        self, business_user: BusinessUserAccountDelete, account: Accounts
    ):
        if not isinstance(account, Business):
            raise NotABusiness()
        business_user = await self.repository.get_business_user_by_id(
            business_user_id=business_user.business_user_id, business_id=account.id
        )
        if business_user is None:
            raise BusinessUserNotFound()
        await self.repository.delete(model_instance=business_user)

    async def get_business_account_info(self, account: Accounts):
        if not isinstance(account, Business):
            raise NotABusiness()
        return account
