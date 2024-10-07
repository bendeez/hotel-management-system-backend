from apps.admin_app.facility.domain.models import Facility
from apps.admin_app.facility.domain.schemas import FacilityCreate
from apps.admin_app.facility.domain.repository import FacilityRepository
from apps.admin_app.accounts.domain.models import Accounts
from apps.admin_app.facility.domain.exceptions import FacilityNotFound
from tools.domain.base_service import BaseService


class FacilityService(BaseService):
    def __init__(self, repository: FacilityRepository):
        self._repository = repository

    async def create_facility(
        self, facility: FacilityCreate, account: Accounts
    ) -> Facility:
        facility = await self._repository.create(
            Facility(**facility.model_dump(), account_id=account.id)
        )
        return facility

    async def get_all_account_facilities(self, account: Accounts) -> list[Facility]:
        facilities = await self._repository.get_all_account_facilities(
            account_id=account.id
        )
        return facilities

    async def delete_account_facility(self, facility_id: int, account: Accounts):
        facility = await self._repository.get_account_facility_by_id(
            account_id=account.id, facility_id=facility_id
        )
        if facility is None:
            raise FacilityNotFound()
        await self._repository.delete(model_instance=facility)
