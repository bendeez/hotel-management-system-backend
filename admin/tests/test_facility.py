from admin.tests.utils import RequestMethod
from admin.app.facility.schemas import FacilityCreate, FacilityOut
from pytest_lazy_fixtures import lf
import pytest


@pytest.mark.parametrize("account", [lf("user"), lf("business"), lf("business_user")])
async def test_create_facility(account, http_request, facility_service):
    tokens, account = account
    facility_config = FacilityCreate(
        title="spa", description="Have a relaxing time"
    ).model_dump()
    response = await http_request(
        path="/facility",
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
        account=account, facility_id=facility.id
    )


@pytest.mark.parametrize("account", [lf("user"), lf("business"), lf("business_user")])
async def test_get_account_facilities(account, http_request, facilities):
    tokens, account = account
    response = await http_request(
        path="/facilities", method=RequestMethod.GET, token=tokens.access_token
    )
    assert response.status_code == 200
    data = response.json()
    facilities = list(
        filter(lambda facility: facility.account_id == account.id, facilities)
    )
    facilities = [FacilityOut(**facility.__dict__) for facility in facilities]
    assert len(data) == len(facilities)
    assert all(FacilityOut(**d) in facilities for d in data)


@pytest.mark.parametrize("account", [lf("user"), lf("business"), lf("business_user")])
async def test_delete_facility(
    account, http_request, create_facility, facility_service
):
    tokens, account = account
    facility = await create_facility(account=account)
    response = await http_request(
        path=f"/facility/{facility.id}",
        method=RequestMethod.DELETE,
        token=tokens.access_token,
    )
    assert response.status_code == 204
    facilities = await facility_service.get_all_account_facilities(account=account)
    assert all(facility.id != _facility.id for _facility in facilities)


@pytest.mark.parametrize("account", [lf("user"), lf("business"), lf("business_user")])
async def test_invalid_delete_facility_with_account_facility_not_exists(
    account, http_request
):
    tokens, _ = account
    response = await http_request(
        path=f"/facility/100",
        method=RequestMethod.DELETE,
        token=tokens.access_token,
    )
    assert response.status_code == 404
