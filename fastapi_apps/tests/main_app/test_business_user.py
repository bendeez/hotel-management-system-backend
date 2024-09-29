from tests.utils import RequestMethod
from app.admin_app.business_user.domain.schemas import BusinessUserAccountOut


async def test_get_business_user_info(http_request, business_user):
    tokens, business_user = business_user
    response = await http_request(
        path="/business-user/me",
        method=RequestMethod.GET,
        token=tokens.access_token,
    )
    assert response.status_code == 200
    data = response.json()
    assert BusinessUserAccountOut(**data) == BusinessUserAccountOut(
        **business_user.__dict__
    )
