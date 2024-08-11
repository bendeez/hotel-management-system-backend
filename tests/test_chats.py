from utils import RequestMethod
from app.chat.models import Sessions


async def test_get_all_chat_logs(http_request, access_token):
    response = await http_request(
        "/chat/chat-logs?limit=100&offset=0&order=desc&order_by=message_time",
        method=RequestMethod.GET,
        token=access_token,
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) <= 100
    assert data[1]["message_time"] > data[50]["message_time"] > data[60]["message_time"]


async def test_get_chat_logs_by_session_id(http_request, access_token, transaction):
    session = await transaction.get_one(model=Sessions)
    response = await http_request(
        f"/chat/chat-logs/{session.session_id}?limit=100&offset=0&order=desc&order_by=message_time",
        method=RequestMethod.GET,
        token=access_token,
    )
    assert response.status_code == 200
    data = response.json()
    assert all(chat["session_id"] == session.session_id for chat in data)
    assert len(data) <= 100
    assert data[1]["message_time"] > data[2]["message_time"]


async def test_get_sessions(http_request, access_token, transaction):
    response = await http_request(
        f"/chat/sessions?limit=100&offset=0&order=desc&order_by=expiry",
        method=RequestMethod.GET,
        token=access_token,
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) <= 100
    assert data[1]["expiry"] > data[2]["expiry"]
