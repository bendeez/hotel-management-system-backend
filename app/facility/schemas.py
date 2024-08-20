from pydantic import BaseModel


class FacilityIn(BaseModel):
    title: str
    description: str
    business_id: int


class FacilityCreate(FacilityIn):
    id: int


class FacilitiesOut(FacilityCreate):
    pass
