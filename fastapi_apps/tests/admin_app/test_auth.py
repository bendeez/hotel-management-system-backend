from apps.admin_app.user.domain.schemas import UserAccountIn
from apps.admin_app.business.domain.schemas import BusinessAccountIn
from apps.admin_app.business_user.domain.schemas import BusinessUserAccountIn
from tests.utils import RequestMethod
from apps.admin_app.auth.domain.schemas import TokenCreate, TokenRequest, AccessToken
from apps.admin_app.auth.domain.constants import TokenType
import pytest
from pytest_lazy_fixtures import lf


async def test_user_login(user, auth_service, http_request, password):
    _, user = user
    response = await http_request(
        path="/login/user",
        method=RequestMethod.POST,
        json=UserAccountIn(email=user.email, password=password).model_dump(),
    )
    assert response.status_code == 200
    data = response.json()
    tokens = TokenCreate(**data)
    account_id = auth_service.get_account_id(
        token=tokens.access_token, _token_type=TokenType.ACCESS_TOKEN
    )
    assert account_id == user.id


async def test_invalid_user_login_with_password(user, http_request):
    _, user = user
    response = await http_request(
        "/login/user",
        method=RequestMethod.POST,
        json=UserAccountIn(email=user.email, password="wrong password").model_dump(),
    )
    assert response.status_code == 401


async def test_invalid_user_login_with_email(http_request, password):
    response = await http_request(
        "/login/user",
        method=RequestMethod.POST,
        json=UserAccountIn(
            email="wrong-email@gmail.com", password=password
        ).model_dump(),
    )
    assert response.status_code == 401


async def test_business_login(business, auth_service, http_request, password):
    _, business = business
    response = await http_request(
        path="/login/business",
        method=RequestMethod.POST,
        json=BusinessAccountIn(email=business.email, password=password).model_dump(),
    )
    assert response.status_code == 200
    data = response.json()
    tokens = TokenCreate(**data)
    account_id = auth_service.get_account_id(
        token=tokens.access_token, _token_type=TokenType.ACCESS_TOKEN
    )
    assert account_id == business.id


async def test_invalid_business_login_with_password(business, http_request):
    _, business = business
    response = await http_request(
        "/login/business",
        method=RequestMethod.POST,
        json=BusinessAccountIn(
            email=business.email, password="wrong password"
        ).model_dump(),
    )
    assert response.status_code == 401


async def test_invalid_business_login_with_email(http_request, password):
    response = await http_request(
        "/login/business",
        method=RequestMethod.POST,
        json=BusinessAccountIn(
            email="wrong-email@gmail.com", password=password
        ).model_dump(),
    )
    assert response.status_code == 401


async def test_business_user_login(business_user, auth_service, http_request, password):
    _, business_user = business_user
    response = await http_request(
        path="/login/business-user",
        method=RequestMethod.POST,
        json=BusinessUserAccountIn(
            email=business_user.email, password=password
        ).model_dump(),
    )
    assert response.status_code == 200
    data = response.json()
    tokens = TokenCreate(**data)
    account_id = auth_service.get_account_id(
        token=tokens.access_token, _token_type=TokenType.ACCESS_TOKEN
    )
    assert account_id == business_user.id


async def test_invalid_business_user_login_with_password(business_user, http_request):
    _, business_user = business_user
    response = await http_request(
        "/login/business-user",
        method=RequestMethod.POST,
        json=UserAccountIn(
            email=business_user.email, password="wrong password"
        ).model_dump(),
    )
    assert response.status_code == 401


async def test_invalid_business_user_login_with_email(http_request, password):
    response = await http_request(
        "/login/business-user",
        method=RequestMethod.POST,
        json=BusinessUserAccountIn(
            email="wrong-email@gmail.com", password=password
        ).model_dump(),
    )
    assert response.status_code == 401


@pytest.mark.parametrize("account", [lf("user"), lf("business"), lf("business_user")])
async def test_get_access_token_with_refresh_token(account, http_request, auth_service):
    tokens, account = account
    response = await http_request(
        "/refresh",
        method=RequestMethod.POST,
        json=TokenRequest(refresh_token=tokens.refresh_token).model_dump(),
    )
    assert response.status_code == 201
    data = response.json()
    access_token = AccessToken(**data).access_token
    account_id = auth_service.get_account_id(
        token=access_token, _token_type=TokenType.ACCESS_TOKEN
    )
    assert account_id == account.id


@pytest.mark.parametrize("account", [lf("user"), lf("business"), lf("business_user")])
async def test_invalid_get_access_token_with_access_token(
    account, http_request, auth_service
):
    tokens, account = account
    response = await http_request(
        "/refresh",
        method=RequestMethod.POST,
        json=TokenRequest(refresh_token=tokens.access_token).model_dump(),
    )
    assert response.status_code == 409


async def test_get_business_info_unauthorized_with_no_token(http_request):
    response = await http_request(path="/business/me", method=RequestMethod.GET)
    assert response.status_code == 401


async def test_get_business_user_info_unauthorized_with_no_token(http_request):
    response = await http_request(path="/business-user/me", method=RequestMethod.GET)
    assert response.status_code == 401


async def test_get_user_info_unauthorized_with_no_token(http_request):
    response = await http_request(path="/user/me", method=RequestMethod.GET)
    assert response.status_code == 401
