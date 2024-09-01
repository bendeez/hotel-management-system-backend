from pydantic import BaseModel


class FacilityCreate(BaseModel):
    title: str
    description: str


class FacilityOut(FacilityCreate):
    id: int
    account_id: int


class FacilityDelete(BaseModel):
    facility_id: int
