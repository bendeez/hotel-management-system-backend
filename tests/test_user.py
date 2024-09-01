from utils import RequestMethod
from app.user.schemas import UserAccountCreate, UserAccountOut


async def test_create_user_account(http_request, password):
    user_config = UserAccountCreate(
        email="user-create@gmail.com", password=password
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
