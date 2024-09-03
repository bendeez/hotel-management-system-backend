import httpx
import pytest
from app.app import app
from app.facility.models import Facility
from app.tools.database import SessionLocal, engine
from app.tools.base_models import BaseMixin
from utils import RequestMethod, http_request, Request, Client
from app.auth.service import AuthService
from app.utils.service import HashService
from app.business.service import BusinessService
from app.user.service import UserService
from app.user.repository import UserRepository
from app.user.models import Users
from app.business.models import Business
from app.business_user.models import Business_Users
from app.business.repository import BusinessRepository
from app.accounts.repository import AccountsRepository
from app.user.schemas import UserAccountCreate
from app.business.schemas import BusinessAccountCreate
from app.business_user.schemas import BusinessUserAccountCreate
from app.session.service import SessionService
from app.session.models import Chat_Sessions
from app.session.repository import SessionRepository
from app.chat.schemas import ChatLogsCreate
from app.chat.service import ChatService
from app.chat.repository import ChatRepository
from app.chat.models import Chat_Logs
from app.facility.service import FacilityService
from app.facility.repository import FacilityRepository
from app.facility.schemas import FacilityCreate
from typing import Optional, Any
from app.auth.schemas import TokenCreate
from datetime import datetime, timedelta
from app.tools.database import get_db
from app.accounts.models import Accounts
from uuid import uuid4


@pytest.fixture(name="db", scope="session", autouse=True)
async def create_db_session():
    async with SessionLocal() as db:
        yield db


@pytest.fixture(autouse=True)
async def override_dependencies(db):
    def get_test_db():
        return db

    app.dependency_overrides[get_db] = get_test_db


@pytest.fixture(scope="session", autouse=True)
async def create_tables(db):
    async with engine.begin() as conn:
        await conn.run_sync(BaseMixin.metadata.drop_all)
        await conn.run_sync(BaseMixin.metadata.create_all)


@pytest.fixture(scope="session")
def auth_service(db):
    return AuthService(repository=AccountsRepository(db=db))


@pytest.fixture(scope="session")
def hash_service():
    return HashService()


@pytest.fixture(scope="session")
def session_service(db):
    return SessionService(repository=SessionRepository(db=db))


@pytest.fixture(scope="session")
def business_service(db):
    return BusinessService(repository=BusinessRepository(db=db))


@pytest.fixture(scope="session")
def user_service(db):
    return UserService(repository=UserRepository(db=db))


@pytest.fixture(scope="session")
def chat_service(db):
    return ChatService(repository=ChatRepository(db=db))


@pytest.fixture(scope="session")
def facility_service(db):
    return FacilityService(repository=FacilityRepository(db=db))


@pytest.fixture(scope="session")
def password():
    return "1234"


@pytest.fixture(scope="session")
async def create_user_account(user_service, password, auth_service):
    async def _create_user_account():
        user_account = await user_service.create_user_account(
            user=UserAccountCreate(email=f"{uuid4()}@gmail.com", password=password)
        )
        tokens = await auth_service.verify_account(
            email=user_account.email, input_password=password
        )
        return tokens, user_account

    return _create_user_account


@pytest.fixture(scope="session")
async def user(create_user_account) -> tuple[TokenCreate, Users]:
    tokens, user_account = await create_user_account()
    return tokens, user_account


@pytest.fixture(scope="session")
async def create_business_account(auth_service, business_service, password):
    async def _create_business_account() -> tuple[TokenCreate, Business]:
        business_account = await business_service.create_business_account(
            business=BusinessAccountCreate(
                email=f"{uuid4()}@gmail.com",
                password=password,
                name="resort and fun",
                location="US",
            )
        )
        tokens = await auth_service.verify_account(
            email=business_account.email, input_password=password
        )
        return tokens, business_account

    return _create_business_account


@pytest.fixture(scope="session")
async def business(
    create_business_account, auth_service, password
) -> tuple[TokenCreate, Business]:
    tokens, business_account = await create_business_account()
    return tokens, business_account


@pytest.fixture(scope="session")
async def create_business_user_account(
    auth_service, business, business_service, password
):
    _, business = business

    async def _create_business_user_account(
        business=business,
    ) -> tuple[TokenCreate, Business_Users]:
        business_user_account = await business_service.create_business_user_account(
            business_user=BusinessUserAccountCreate(
                email=f"{uuid4()}@gmail.com",
                password=password,
                role_name="admin",
                business_id=business.id,
            ),
            account=business,
        )
        tokens = await auth_service.verify_account(
            email=business_user_account.email, input_password=password
        )
        return tokens, business_user_account

    return _create_business_user_account


@pytest.fixture(scope="session")
async def business_user(
    create_business_user_account,
) -> tuple[TokenCreate, Business_Users]:
    tokens, business_account = await create_business_user_account()
    return tokens, business_account


@pytest.fixture(scope="session")
def user_request():
    return Request(
        client=Client(host="127.0.0.1"), headers={"User-Agent": "Mozilla/5.0"}
    )


@pytest.fixture(scope="session")
async def create_session(session_service, user_request):
    async def _create_session(account: Accounts) -> Chat_Sessions:
        session = await session_service.create_chat_session(
            account=account, request=user_request
        )
        return session

    return _create_session


@pytest.fixture(scope="session")
async def sessions(
    create_session, user, business, business_user
) -> list[Chat_Sessions]:
    sessions = []
    for account in [user, business, business_user]:
        _, account = account
        """
            2 sessions created for each account
            not counting the expired ones
        """
        for i in range(2):
            session = await create_session(account=account)
            sessions.append(session)
    return sessions


@pytest.fixture(scope="session")
async def expired_sessions(
    db, session_service, user, business, business_user, user_request
) -> list[Chat_Sessions]:
    expired_sessions = []
    for account in [user, business, business_user]:
        _, account = account
        session = await session_service.create_chat_session(
            account=account, request=user_request
        )
        session.end_time = datetime.now() - timedelta(hours=24)
        expired_sessions.append(session)
    await db.commit()
    return expired_sessions


@pytest.fixture(scope="session")
async def create_chat_log(chat_service):
    async def _create_chat_log(session: Chat_Sessions, account: Accounts):
        chat_log = await chat_service.create_chat_log(
            account=account,
            chat_log=ChatLogsCreate(session_id=session.id, message=str(uuid4())),
        )
        return chat_log

    return _create_chat_log


@pytest.fixture(scope="session")
async def chat_logs(
    sessions, create_chat_log, user, business, business_user
) -> list[Chat_Logs]:
    chat_logs = []
    for session in sessions:
        account = (
            user[1]
            if user[1].id == session.account_id
            else business[1]
            if business[1].id == session.account.id
            else business_user[1]
        )
        """
            each account has 2 sessions so it will create 6 (2 * 3) 
            chat logs total per account
        """
        for _ in range(3):
            chat_log = await create_chat_log(account=account, session=session)
            chat_logs.append(chat_log)
    return chat_logs


@pytest.fixture(scope="session")
async def create_facility(facility_service):
    async def _create_facility(account: Accounts) -> Facility:
        facility = await facility_service.create_facility(
            FacilityCreate(title=str(uuid4()), description=str(uuid4())),
            account=account,
        )
        return facility

    return _create_facility


@pytest.fixture(scope="session")
async def facilities(create_facility, user, business, business_user) -> list[Facility]:
    facilities = []
    for account in [user, business, business_user]:
        _, account = account
        """
            3 facilities are created for each account
        """
        for i in range(3):
            facility = await create_facility(account=account)
            facilities.append(facility)
    return facilities


@pytest.fixture(scope="session", name="client", autouse=True)
async def create_http_client():
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(
        transport=transport, base_url="http://127.0.0.1:8000"
    ) as client:
        yield client


@pytest.fixture(name="http_request")
async def make_http_request(client):
    async def _make_http_request(
        path,
        client=client,
        method=RequestMethod.GET,
        json: Optional[dict] = None,
        files=None,
        token: Optional[str] = None,
        params: Optional[dict] = None,
    ):
        data = await http_request(
            client=client,
            path=path,
            method=method,
            json=json,
            files=files,
            token=token,
            params=params,
        )
        return data

    return _make_http_request


@pytest.fixture(scope="session", autouse=True)
def anyio_backend():
    return "asyncio"
