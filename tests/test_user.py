from utils import RequestMethod
from app.user.schemas import UserAccountCreate, UserAccountOut
import pytest
from app.auth.exceptions import AdminUnauthorized
from uuid import uuid4


async def test_create_user_account(http_request, password):
    user_config = UserAccountCreate(
        email=f"{uuid4()}@gmail.com", password=password
    ).model_dump()
    response = await http_request(
        path="/user", method=RequestMethod.POST, json=user_config
    )
    assert response.status_code == 201
    data = response.json()
    user_account = UserAccountOut(**data)
    assert user_account == UserAccountOut(id=user_account.id, **user_config)


async def test_invalid_create_user_account_with_email_already_exists(
    user, http_request, password
):
    _, user = user
    user_config = UserAccountCreate(email=user.email, password=password).model_dump()
    response = await http_request(
        path="/user", method=RequestMethod.POST, json=user_config
    )
    assert response.status_code == 409


async def test_delete_user_account(
    create_user_account,
    http_request,
    auth_service,
    password,
):
    tokens, user = await create_user_account()
    response = await http_request(
        path="/user",
        method=RequestMethod.DELETE,
        token=tokens.access_token,
    )
    assert response.status_code == 204
    with pytest.raises(AdminUnauthorized):
        await auth_service.verify_account(email=user.email, input_password=password)


async def test_get_user_info(http_request, user):
    tokens, user = user
    response = await http_request(
        path="/user/me",
        method=RequestMethod.GET,
        token=tokens.access_token,
    )
    assert response.status_code == 200
    data = response.json()
    assert UserAccountOut(**data) == UserAccountOut(**user.__dict__)


async def test_get_user_info_unauthorized_with_no_token(http_request):
    response = await http_request(path="/user/me", method=RequestMethod.GET)
    assert response.status_code == 401
