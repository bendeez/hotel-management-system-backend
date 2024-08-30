from fastapi import Depends
from app.facility.models import Facility
from app.facility.schemas import FacilityCreate
from app.facility.repository import FacilityRepository


class FacilityService:

    def __init__(self, repository: FacilityRepository = Depends(FacilityRepository)):
        self.repository = repository

    async def create_facility(self, facility: FacilityCreate):
        facility = await self.repository.create(Facility(**facility.model_dump()))
        return facility

    async def get_all_facilities(self):
        facilities = await self.repository.get_all_facilities()
        return facilities
