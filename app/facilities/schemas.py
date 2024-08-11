from pydantic import BaseModel


class FacilityIn(BaseModel):
    title: str
    description: str


class FacilityCreate(FacilityIn):
    id: int


class FacilitiesOut(FacilityCreate):
    pass
