from app.tools.base_service import BaseService
from app.facilities.models import Facility
from app.facilities.schemas import FacilityIn


class FacilitiesService(BaseService):
    async def create_facility(self, facility: FacilityIn):
        new_facility = await self.transaction.create(
            model=Facility, **facility.model_dump()
        )
        return new_facility

    async def get_all_facilities(self):
        facilities = await self.transaction.get_all(model=Facility)
        return facilities
