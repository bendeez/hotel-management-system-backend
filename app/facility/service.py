from app.facility.models import Facility
from app.facility.schemas import FacilityIn


class FacilityService:
    def create_facility(self, facility: FacilityIn):
        return Facility(**facility.model_dump())
