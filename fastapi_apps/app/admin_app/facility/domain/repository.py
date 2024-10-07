from tools.domain.base_repository import BaseRepository
from app.admin_app.facility.domain.models import Facility
from app.admin_app.accounts.domain.models import Accounts
from sqlalchemy.sql.elements import BinaryExpression


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
