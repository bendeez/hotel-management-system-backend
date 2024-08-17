from fastapi import APIRouter, Depends, status
from app.facilities.schemas import FacilityIn, FacilityCreate, FacilitiesOut
from app.facilities.service import FacilitiesService
from typing import List


facilities_router = APIRouter(prefix="/facilities")


@facilities_router.post(
    "/", response_model=FacilityCreate, status_code=status.HTTP_201_CREATED
)
async def create_facility(
    facility: FacilityIn,
    facilities_service: FacilitiesService = Depends(FacilitiesService),
):
    new_info = await facilities_service.create_facility(facility=facility)
    return new_info


@facilities_router.get("/", response_model=List[FacilitiesOut])
async def get_facilities(
    facilities_service: FacilitiesService = Depends(FacilitiesService),
):
    facilities = await facilities_service.get_all_facilities()
    return facilities


