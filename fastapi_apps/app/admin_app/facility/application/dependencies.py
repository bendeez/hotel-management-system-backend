from fastapi import Depends
from app.admin_app.facility.domain.repository import FacilityRepository
from app.admin_app.facility.domain.service import FacilityService
from app.tools.application.dependencies import get_db
from sqlalchemy.ext.asyncio import AsyncSession


def _get_facility_repository(db: AsyncSession = Depends(get_db)) -> FacilityRepository:
    return FacilityRepository(db=db)


def get_facility_service(
    facility_repository: FacilityRepository = Depends(_get_facility_repository),
) -> FacilityService:
    return FacilityService(repository=facility_repository)
