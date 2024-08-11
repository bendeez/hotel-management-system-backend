from utils import RequestMethod


async def test_get_admin_user(access_token, http_request, admin_user):
    response = await http_request(
        "/user/me", method=RequestMethod.GET, token=access_token
    )
    assert response.status_code == 200
    data = response.json()
    assert data == {
        "id": admin_user.id,
        "email": admin_user.email,
        "role": admin_user.role,
    }
