from app.tools.base_service import BaseService
from app.business.schemas import BusinessAccountCreate
from app.business.models import Business

class BusinessService(BaseService):

    async def create_business_account(self, account: BusinessAccountCreate):
        new_business = await self.transaction.create(model=Business, **account.model_dump(), )