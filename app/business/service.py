from fastapi import Depends
from app.tools.base_service import BaseService
from app.business.models import Business
from app.business.schemas import BusinessAccountCreate
from app.utils.service import HashService
from app.tools.db.database_transaction import DatabaseTransactionService
from app.business.exceptions import BusinessEmailAlreadyExists


class BusinessService(BaseService):
    def __init__(
        self,
        transaction: DatabaseTransactionService = Depends(DatabaseTransactionService),
    ):
        super().__init__(transaction=transaction)
        self.hash_service = HashService()

    async def create_business_account(self, business: BusinessAccountCreate):
        existing_business = await self.get_business_by_email(email=business.email)
        if existing_business is not None:
            raise BusinessEmailAlreadyExists()
        business.password = self.hash_service.hash(business.password)
        business_account = await self.transaction.create(
            model=Business, **business.model_dump()
        )
        return business_account

    async def get_business_by_email(self, email: str):
        business = await self.transaction.get_one(
            model=Business, filter={Business.email: email}
        )
        return business

    async def get_business_by_id(self, business_id: int):
        business = await self.transaction.get_one(
            model=Business, filter={Business.id: business_id}
        )
        return business
