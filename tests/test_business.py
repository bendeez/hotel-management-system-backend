from app.business.schemas import BusinessAccountCreate, BusinessAccountOut
from app.business_user.schemas import BusinessUserAccountCreate, BusinessUserAccountOut
from utils import RequestMethod


async def test_create_business_account(http_request, password):
    business_config = BusinessAccountCreate(
        email="business-create@gmail.com",
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

async def test_delete_business_account(business, http_request):
    tokens, business = business
    response = await http_request(
        path="/business", method=RequestMethod.DELETE,
        token=tokens.refresh_token
    )
    assert response.status_code == 200

async def test_create_business_user_account(business, http_request, password):
    tokens, business = business
    business_user_config = BusinessUserAccountCreate(
        email="business-user-create@gmail.com",
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
        email="business-user-create@gmail.com",
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
