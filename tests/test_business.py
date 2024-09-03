import pytest
from app.auth.exceptions import AdminUnauthorized
from app.business.schemas import BusinessAccountCreate, BusinessAccountOut
from app.business_user.schemas import BusinessUserAccountCreate, BusinessUserAccountOut
from app.business_user.schemas import BusinessUserAccountDelete
from utils import RequestMethod
from uuid import uuid4


async def test_create_business_account(http_request, password):
    business_config = BusinessAccountCreate(
        email=f"{uuid4()}@gmail.com",
        password=password,
        name="resort and fun",
        location="US",
    ).model_dump()
    response = await http_request(
        path="/business", method=RequestMethod.POST, json=business_config
    )
    assert response.status_code == 201
    data = response.json()
    business_account = BusinessAccountOut(**data)
    assert business_account == BusinessAccountOut(
        id=business_account.id, **business_config
    )


async def test_create_business_account_with_email_already_exists(
    business, http_request, password
):
    _, business = business
    business_config = BusinessAccountCreate(
        email=business.email, password=password, name="resort and fun", location="US"
    ).model_dump()
    response = await http_request(
        path="/business", method=RequestMethod.POST, json=business_config
    )
    assert response.status_code == 409


async def test_delete_business_account(
    refresh_session,
    create_business_account,
    http_request,
    business_service,
    auth_service,
    password,
):
    tokens, business = await create_business_account()
    response = await http_request(
        path="/business", method=RequestMethod.DELETE, token=tokens.access_token
    )
    assert response.status_code == 204
    await refresh_session()
    with pytest.raises(AdminUnauthorized):
        await auth_service.verify_account(email=business.email, input_password=password)


async def test_create_business_user_account(business, http_request, password):
    tokens, business = business
    business_user_config = BusinessUserAccountCreate(
        email=f"{uuid4()}@gmail.com",
        password=password,
        role_name="admin",
        business_id=business.id,
    ).model_dump()
    response = await http_request(
        path="/business/add-account",
        method=RequestMethod.POST,
        json=business_user_config,
        token=tokens.access_token,
    )
    assert response.status_code == 201
    data = response.json()
    business_user_account = BusinessUserAccountOut(**data)
    assert business_user_account == BusinessUserAccountOut(
        id=business_user_account.id, **business_user_config
    )


async def test_invalid_create_business_user_account_with_invalid_account_type(
    user, http_request, password
):
    tokens, user = user
    business_user_config = BusinessUserAccountCreate(
        email=f"{uuid4()}@gmail.com",
        password=password,
        role_name="admin",
        business_id=user.id,
    ).model_dump()
    response = await http_request(
        path="/business/add-account",
        method=RequestMethod.POST,
        json=business_user_config,
        token=tokens.access_token,
    )
    assert response.status_code == 403


async def test_invalid_create_business_user_account_with_email_already_exists(
    business, business_user, http_request, password
):
    tokens, business = business
    _, business_user = business_user
    business_user_config = BusinessUserAccountCreate(
        email=business_user.email,
        password=password,
        role_name="admin",
        business_id=business.id,
    ).model_dump()
    response = await http_request(
        path="/business/add-account",
        method=RequestMethod.POST,
        json=business_user_config,
        token=tokens.access_token,
    )
    assert response.status_code == 409


async def test_delete_business_user_account(
    refresh_session,
    business,
    create_business_user_account,
    http_request,
    auth_service,
    password,
):
    _, business_user = await create_business_user_account()
    tokens, business = business
    business_user_config = BusinessUserAccountDelete(
        business_user_id=business_user.id
    ).model_dump()
    response = await http_request(
        path="/business/remove-account",
        method=RequestMethod.DELETE,
        json=business_user_config,
        token=tokens.access_token,
    )
    assert response.status_code == 204
    await refresh_session()
    with pytest.raises(AdminUnauthorized):
        await auth_service.verify_account(
            email=business_user.email, input_password=password
        )


async def test_invalid_delete_business_user_account_not_linked_to_business(
    business, http_request
):
    tokens, _ = business
    business_user_config = BusinessUserAccountDelete(business_user_id=100).model_dump()
    response = await http_request(
        path="/business/remove-account",
        method=RequestMethod.DELETE,
        json=business_user_config,
        token=tokens.access_token,
    )
    assert response.status_code == 404
