from fastapi import APIRouter, Depends, status
from app.facility.schemas import FacilityCreate, FacilityOut
from typing import List
from app.facility.service import FacilityService
from app.facility.repository import FacilityRepository
from app.auth.account import get_account
from app.accounts.models import Accounts


facility_router = APIRouter(prefix="/facility")


@facility_router.post(
    "/", response_model=FacilityOut, status_code=status.HTTP_201_CREATED
)
async def create_facility(
    facility: FacilityCreate,
    facility_service: FacilityService = Depends(FacilityService),
    account: Accounts = Depends(get_account),
):
    facility = await facility_service.create_facility(facility=facility)
    return facility


@facility_router.get("/", response_model=List[FacilityOut])
async def get_facilities(
    facility_service: FacilityService = Depends(FacilityService),
    account: Accounts = Depends(get_account),
):
    facilities = await facility_service.get_all_facilities()
    return facilities
