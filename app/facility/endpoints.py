from fastapi import APIRouter, Depends, status
from app.facility.schemas import FacilityIn, FacilityCreate, FacilityOut
from typing import List
from app.facility.service import FacilityService
from app.facility.repository import FacilityRepository
from app.auth.account import get_account
from app.accounts.models import Accounts


facility_router = APIRouter(prefix="/facility")


@facility_router.post(
    "/", response_model=FacilityCreate, status_code=status.HTTP_201_CREATED
)
async def create_facility(
    facility: FacilityIn,
    facility_service: FacilityService = Depends(FacilityService),
    facility_repository: FacilityRepository = Depends(FacilityRepository),
    account: Accounts = Depends(get_account),
):
    facility = facility_service.create_facility(facility=facility)
    saved_facility = await facility_repository.create(facility)
    return saved_facility


@facility_router.get("/", response_model=List[FacilityOut])
async def get_facilities(
    facility_repository: FacilityRepository = Depends(FacilityRepository),
    account: Accounts = Depends(get_account),
):
    facilities = await facility_repository._get_all_facilities()
    return facilities
