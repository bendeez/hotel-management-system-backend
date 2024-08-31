from pydantic import BaseModel


class FacilityCreate(BaseModel):
    title: str
    description: str
    account_id: int


class FacilityOut(FacilityCreate):
    id: int
