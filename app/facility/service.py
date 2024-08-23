from app.facility.models import Facility
from app.facility.schemas import FacilityCreate


class FacilityService:
    def create_facility(self, facility: FacilityCreate):
        return Facility(**facility.model_dump())
