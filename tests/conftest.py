import httpx
import pytest
from app.app import app
from app.tools.database import SessionLocal, engine
from app.tools.base_models import BaseMixin
from utils import RequestMethod, http_request
from app.auth.service import AuthService
from app.utils.service import HashService
from app.business.service import BusinessService
from app.user.service import UserService
from app.user.repository import UserRepository
from app.user.models import Users
from app.business.models import Business, Business_Users
from app.business.repository import BusinessRepository
from app.accounts.repository import AccountsRepository
from app.user.schemas import UserAccountCreate
from app.business.schemas import BusinessAccountCreate, BusinessUserAccountCreate
from app.auth.schemas import TokenCreate


@pytest.fixture(name="db", scope="session", autouse=True)
async def create_db_session():
    async with SessionLocal() as db:
        yield db


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
def business_service(db):
    return BusinessService(repository=BusinessRepository(db=db))


@pytest.fixture(scope="session")
def user_service(db):
    return UserService(repository=UserRepository(db=db))


@pytest.fixture(scope="session")
def password():
    return "1234"


@pytest.fixture(scope="session")
async def user(user_service, password, auth_service) -> tuple[TokenCreate, Users]:
    user_account = await user_service.create_user_account(
        user=UserAccountCreate(email="user@gmail.com", password=password)
    )
    tokens = await auth_service.verify_account(
        email=user_account.email, input_password=password
    )
    return tokens, user_account


@pytest.fixture(scope="session")
async def business(
    business_service, password, auth_service
) -> tuple[TokenCreate, Business]:
    business_account = await business_service.create_business_account(
        business=BusinessAccountCreate(
            email="business@gmail.com",
            password=password,
            name="resort and fun",
            location="US",
        )
    )
    tokens = await auth_service.verify_account(
        email=business_account.email, input_password=password
    )
    return tokens, business_account


@pytest.fixture(scope="session")
async def business_user(
    business, business_service, password, auth_service
) -> tuple[TokenCreate, Business_Users]:
    tokens, business = business
    business_user_account = await business_service.create_business_user_account(
        business_user=BusinessUserAccountCreate(
            email="business-user@gmail.com",
            password=password,
            role_name="admin",
            business_id=business.id,
        )
    )
    tokens = await auth_service.verify_account(
        email=business_user_account.email, input_password=password
    )
    return tokens, business_user_account


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
        path, client=client, method=RequestMethod.GET, json=None, files=None, token=None
    ):
        data = await http_request(
            client=client, path=path, method=method, json=json, files=files, token=token
        )
        return data

    return _make_http_request


@pytest.fixture(scope="session", autouse=True)
def anyio_backend():
    return "asyncio"
