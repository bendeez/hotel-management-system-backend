from fastapi import Depends
from app.facility.models import Facility
from app.facility.schemas import FacilityCreate
from app.facility.repository import FacilityRepository
from app.accounts.models import Accounts


class FacilityService:
    def __init__(self, repository: FacilityRepository = Depends(FacilityRepository)):
        self.repository = repository

    async def create_facility(
        self, facility: FacilityCreate, account: Accounts
    ) -> Facility:
        facility = await self.repository.create(
            Facility(**facility.model_dump(), account_id=account.id)
        )
        return facility

    async def get_all_account_facilities(self, account: Accounts) -> list[Facility]:
        facilities = await self.repository.get_all_account_facilities(
            account_id=account.id
        )
        return facilities
