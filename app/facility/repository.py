from app.tools.base_repository import BaseRepository
from app.facility.models import Facility


class FacilityRepository(BaseRepository):
    async def get_all_account_facilities(self, account_id: int) -> list[Facility]:
        facilities = await self._get_all(
            model=Facility, filters=[Facility.account_id == account_id]
        )
        return facilities
