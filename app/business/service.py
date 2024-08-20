from app.business.models import Business, Business_Users, Accounts
from app.business.schemas import BusinessAccountCreate, BusinessUserAccountCreate
from app.utils.service import HashService
from app.business.exceptions import (
    BusinessEmailAlreadyExists,
    NotABusiness,
    BusinessForbidden,
    BusinessUserEmailAlreadyExists,
)


class BusinessService:
    def __init__(self):
        self.hash_service = HashService()

    def create_business_account(
        self, business: BusinessAccountCreate, business_exists: bool
    ):
        if business_exists:
            raise BusinessEmailAlreadyExists()
        business.password = self.hash_service.hash(business.password)
        return Business(**business.model_dump())

    async def create_business_user_account(
        self,
        account: Accounts,
        business_user: BusinessUserAccountCreate,
        business_user_exists: bool,
    ):
        if not isinstance(account, Business):
            raise NotABusiness()
        if account.id != business_user.business_id:
            raise BusinessForbidden()
        if business_user_exists:
            raise BusinessUserEmailAlreadyExists()
        business_user.password = self.hash_service.hash(business_user.password)
        return Business_Users(**business_user.model_dump())
