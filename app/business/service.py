from app.tools.base_service import BaseService
from app.business.models import Business
from app.business.schemas import BusinessAccountCreate

class BusinessService(BaseService):

    async def create_business(self, business: BusinessAccountCreate, account_id: int):
        business_account = await self.transaction.create(model=Business, **business.model_dump(),
                                                         account_id=account_id)
        return business_account
