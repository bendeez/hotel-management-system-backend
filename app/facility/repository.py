from app.tools.base_repository import BaseRepository
from app.facility.models import Facility


class FacilityRepository(BaseRepository):
    async def _get_all_facilities(self):
        facilities = await self._get_all(model=Facility)
        return facilities
