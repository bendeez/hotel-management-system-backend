from app.tools.base_repository import BaseRepository
from app.facility.models import Facility


class FacilityRepository(BaseRepository):
    async def get_all_facilities(self):
        facilities = await self.get_all(model=Facility)
        return facilities
