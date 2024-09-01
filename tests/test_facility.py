from utils import RequestMethod
from app.facility.schemas import FacilityCreate, FacilityOut, FacilityDelete
from app.facility.models import Facility
from pytest_lazy_fixtures import lf
import pytest


@pytest.mark.parametrize("account", [lf("user"), lf("business"), lf("business_user")])
async def test_create_facility(account, http_request, facility_service):
    tokens, account = account
    facility_config = FacilityCreate(
        title="spa", description="Have a relaxing time"
    ).model_dump()
    response = await http_request(
        path="/facility/facility",
        method=RequestMethod.POST,
        json=facility_config,
        token=tokens.access_token,
    )
    assert response.status_code == 201
    data = response.json()
    facility = FacilityOut(**data)
    assert facility == FacilityOut(
        id=facility.id, account_id=account.id, **facility_config
    )
    await facility_service.delete_account_facility(
        account=account, facility=FacilityDelete(facility_id=facility.id)
    )


@pytest.mark.parametrize("account", [lf("user"), lf("business"), lf("business_user")])
async def test_get_account_facilities(account, http_request, facilities):
    tokens, account = account
    response = await http_request(
        path="/facility/facilities", method=RequestMethod.GET, token=tokens.access_token
    )
    assert response.status_code == 200
    data = response.json()
    facilities = list(
        filter(lambda facility: facility.account_id == account.id, facilities)
    )
    facilities = [FacilityOut(**facility) for facility in facilities]
    assert len(data) == len(facilities)
    assert all(FacilityOut(**d) in facilities for d in data)
