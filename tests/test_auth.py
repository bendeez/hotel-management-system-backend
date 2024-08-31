from app.user.schemas import UserAccountIn
from utils import RequestMethod


async def test_user_login(http_request, password, user):
    _, user = user
    response = await http_request("/login/user", method=RequestMethod.POST,
                                  json=UserAccountIn(email=user.email, password=password).model_dump())
    assert response.status_code == 200