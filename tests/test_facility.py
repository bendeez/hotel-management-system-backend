from app.facility.schemas import FacilityCreate, FacilityOut
import pytest
from pytest_lazy_fixtures import lf
from pydantic import ValidationError

@pytest.mark.parametrize("account", [lf("user"), lf("business"), lf("business_user")])
def test_facility_creation(account, facility_service):
    _, account = account
    facility_info = FacilityCreate(title="spa",description="place to relax", account_id=account.id)
    facility = facility_service.create_facility(facility=facility_info)
    assert FacilityOut(id=1, **facility.__dict__) == FacilityOut(id=1, **facility_info.model_dump())

def test_invalid_facility_creation_with_invalid_fields():
    with pytest.raises(ValidationError):
        FacilityCreate(title="spa", description="place to relax") # missing account id
