from app.tools.domain.base_repository import BaseRepository
from app.facility.domain.models import Facility


class FacilityRepository(BaseRepository):
    async def get_all_account_facilities(self, account_id: int) -> list[Facility]:
        facilities = await self._get_all(
            model=Facility, filters=[Facility.account_id == account_id]
        )
        return facilities

    async def get_account_facility_by_id(
        self, account_id: int, facility_id: int
    ) -> Facility:
        facility = await self._get_one(
            model=Facility,
            filters=[Facility.account_id == account_id, Facility.id == facility_id],
        )
        return facility
