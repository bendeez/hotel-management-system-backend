from tests.utils import RequestMethod
from app.chat.domain.schemas import ChatLogsCreate, ChatLogsOut
import pytest
from pytest_lazy_fixtures import lf


@pytest.mark.parametrize("account", [lf("user"), lf("business"), lf("business_user")])
async def test_create_chat_log(
    account, http_request, sessions, user_request, chat_service
):
    tokens, account = account
    """
        gets first session by account id
    """
    session = next(filter(lambda session: session.account_id == account.id, sessions))
    chat_log_info = ChatLogsCreate(session_id=session.id, message="hello").model_dump()
    response = await http_request(
        path="/chat-log",
        method=RequestMethod.POST,
        json=chat_log_info,
        token=tokens.access_token,
    )
    assert response.status_code == 201
    data = response.json()
    chat_log = ChatLogsOut(**data)
    assert chat_log == ChatLogsOut(
        id=chat_log.id,
        date=chat_log.date,
        ip_address=user_request.client,
        user_agent=user_request.headers["User-Agent"],
        **chat_log_info,
    )
    await chat_service.delete_chat_log(account=account, chat_log_id=chat_log.id)


@pytest.mark.parametrize("account", [lf("user"), lf("business"), lf("business_user")])
async def test_invalid_create_chat_log_with_invalid_session_id(account, http_request):
    tokens, account = account
    chat_log_info = ChatLogsCreate(session_id="4595959", message="hello").model_dump()
    response = await http_request(
        path="/chat-log",
        method=RequestMethod.POST,
        json=chat_log_info,
        token=tokens.access_token,
    )
    assert response.status_code == 404


@pytest.mark.parametrize("account", [lf("user"), lf("business"), lf("business_user")])
async def test_invalid_create_chat_log_with_unauthorized_session_id(
    account, http_request, sessions
):
    tokens, account = account
    """
        gets first session not equal to the account id
    """
    session = next(
        filter(lambda session: session.account_id != account.id, sessions)
    )  # note !=
    chat_log_info = ChatLogsCreate(session_id=session.id, message="hello").model_dump()
    response = await http_request(
        path="/chat-log",
        method=RequestMethod.POST,
        json=chat_log_info,
        token=tokens.access_token,
    )
    assert response.status_code == 403


@pytest.mark.parametrize("account", [lf("user"), lf("business"), lf("business_user")])
async def test_invalid_create_chat_log_with_expired_session(
    account, http_request, expired_sessions, user_request
):
    tokens, account = account
    """
        gets first session by account id
    """
    session = next(
        filter(lambda session: session.account_id == account.id, expired_sessions)
    )
    chat_log_info = ChatLogsCreate(session_id=session.id, message="hello").model_dump()
    response = await http_request(
        path="/chat-log",
        method=RequestMethod.POST,
        json=chat_log_info,
        token=tokens.access_token,
    )
    assert response.status_code == 404


@pytest.mark.parametrize("account", [lf("user"), lf("business"), lf("business_user")])
async def test_get_account_chat_logs(account, http_request, chat_logs, sessions):
    tokens, account = account
    params = {"limit": 2, "offset": 0, "order": "desc", "order_by": "date"}
    response = await http_request(
        path="/chat-logs",
        params=params,
        method=RequestMethod.GET,
        token=tokens.access_token,
    )
    assert response.status_code == 200
    data = response.json()
    chat_logs = [ChatLogsOut(**d) for d in data]
    assert len(chat_logs) <= params["limit"]
    assert chat_logs[0].date >= chat_logs[1].date
    """
        gets session for each chat log and checks that the session
        account id is equal to the account id that made the request
    """
    assert all(
        next(
            filter(lambda session: session.id == chat_log.session_id, sessions)
        ).account_id
        == account.id
        for chat_log in chat_logs
    )


@pytest.mark.parametrize("account", [lf("user"), lf("business"), lf("business_user")])
async def test_get_account_chat_logs_by_session_id(
    account, http_request, chat_logs, sessions
):
    tokens, account = account
    session = next(filter(lambda session: session.account_id == account.id, sessions))
    params = {"limit": 2, "offset": 0, "order": "desc", "order_by": "date"}
    response = await http_request(
        path=f"/chat-logs/{session.id}",
        params=params,
        method=RequestMethod.GET,
        token=tokens.access_token,
    )
    assert response.status_code == 200
    data = response.json()
    chat_logs = [ChatLogsOut(**d) for d in data]
    assert len(chat_logs) <= params["limit"]
    assert chat_logs[0].date >= chat_logs[1].date
    assert session.account_id == account.id
    assert all(chat_log.session_id == session.id for chat_log in chat_logs)


@pytest.mark.parametrize("account", [lf("user"), lf("business"), lf("business_user")])
async def test_delete_chat_log(
    account, http_request, chat_service, create_chat_log, sessions
):
    tokens, account = account
    session = next(filter(lambda session: session.account_id == account.id, sessions))
    chat_log = await create_chat_log(session=session, account=account)
    response = await http_request(
        path=f"/chat-log/{chat_log.id}",
        method=RequestMethod.DELETE,
        token=tokens.access_token,
    )
    assert response.status_code == 204
    chat_logs = await chat_service.get_chat_logs_by_session_id(
        session_id=session.id, account=account
    )
    assert all(chat_log.id != _chat_log.id for _chat_log in chat_logs)


@pytest.mark.parametrize("account", [lf("user"), lf("business"), lf("business_user")])
async def test_invalid_delete_chat_log_with_account_chat_log_not_exists(
    account, http_request
):
    tokens, _ = account
    response = await http_request(
        path=f"/chat-log/100",
        method=RequestMethod.DELETE,
        token=tokens.access_token,
    )
    assert response.status_code == 404
