from pydantic import BaseModel


class FacilityCreate(BaseModel):
    title: str
    description: str


class FacilityOut(FacilityCreate):
    id: int
    account_id: int
