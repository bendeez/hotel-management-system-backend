from fastapi import APIRouter, Depends, status, Request
from app.facility.domain.schemas import FacilityCreate, FacilityOut
from typing import List
from app.facility.domain.service import FacilityService
from app.auth.application.dependencies import get_account
from app.accounts.domain.models import Accounts
from app.facility.application.dependencies import get_facility_service
from app.tools.application.rate_limiter import limiter, limit


facility_router = APIRouter()


@facility_router.post(
    "/facility", response_model=FacilityOut, status_code=status.HTTP_201_CREATED
)
@limiter.limit(limit)
async def create_facility(
    request: Request,
    facility: FacilityCreate,
    facility_service: FacilityService = Depends(get_facility_service),
    account: Accounts = Depends(get_account),
):
    facility = await facility_service.create_facility(
        facility=facility, account=account
    )
    return facility


@facility_router.get("/facilities", response_model=List[FacilityOut])
@limiter.limit(limit)
async def get_account_facilities(
    request: Request,
    facility_service: FacilityService = Depends(get_facility_service),
    account: Accounts = Depends(get_account),
):
    facilities = await facility_service.get_all_account_facilities(account=account)
    return facilities


@facility_router.delete(
    "/facility/{facility_id}", status_code=status.HTTP_204_NO_CONTENT
)
@limiter.limit(limit)
async def delete_facility(
    request: Request,
    facility_id: int,
    facility_service: FacilityService = Depends(get_facility_service),
    account: Accounts = Depends(get_account),
):
    await facility_service.delete_account_facility(
        facility_id=facility_id, account=account
    )
