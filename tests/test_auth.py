from utils import RequestMethod


async def test_admin_login(admin_user, http_request, auth_service):
    response = await http_request(
        "/login",
        method=RequestMethod.POST,
        json={"email": admin_user.email, "password": admin_user.password},
    )
    assert response.status_code == 200
    data = response.json()
    access_token_payload = auth_service.decode(data["access_token"])
    del access_token_payload["exp"]
    refresh_token_payload = auth_service.decode(data["refresh_token"])
    del refresh_token_payload["exp"]
    assert access_token_payload == {
        "user_id": admin_user.id,
        "token_type": "access_token",
    }
    assert refresh_token_payload == {
        "user_id": admin_user.id,
        "token_type": "refresh_token",
    }


async def test_invalid_normal_user_login(normal_user, http_request):
    """
    only admins allowed
    """
    response = await http_request(
        "/login",
        method=RequestMethod.POST,
        json={"email": normal_user.email, "password": normal_user.password},
    )
    assert response.status_code == 401


async def test_login_invalid_credentials(admin_user, http_request):
    response = await http_request(
        "/login",
        method=RequestMethod.POST,
        json={"email": admin_user.email, "password": "39883457854"},
    )
    assert response.status_code == 401


async def test_refresh(refresh_token, admin_user, http_request, auth_service):
    response = await http_request(
        "/refresh", method=RequestMethod.POST, json={"refresh_token": refresh_token}
    )
    assert response.status_code == 201
    data = response.json()
    access_token_payload = auth_service.decode(data["access_token"])
    del access_token_payload["exp"]
    assert access_token_payload == {
        "user_id": admin_user.id,
        "token_type": "access_token",
    }


async def test_invalid_refresh_with_access_token(
    access_token, admin_user, http_request, auth_service
):
    """
        access token cannot be used to get another access token
    :param admin_user:
    :param http_request:
    :param auth_service:
    :return:
    """
    response = await http_request(
        "/refresh", method=RequestMethod.POST, json={"refresh_token": access_token}
    )
    assert response.status_code == 409


async def test_invalid_protected_route_request_with_refresh_token(
    admin_user, http_request, refresh_token
):
    """
        refresh token is not used for authentication
    :param admin_user:
    :param http_request:
    :param refresh_token:
    :return:
    """
    response = await http_request(
        "/user/me", method=RequestMethod.GET, token=refresh_token
    )
    assert response.status_code == 401
