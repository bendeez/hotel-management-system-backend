import pytest
import httpx
from app.app import app
from app.user.service import UserService
from app.tools.db.database import SessionLocal
from app.tools.db.database_transaction import DatabaseTransactionService
from app.
from app.auth.service import AuthService, HashService
from utils import http_request, RequestMethod
from app.user.models import Users
from utils import UserMock


@pytest.fixture(name="transaction", scope="session", autouse=True)
async def create_db_session():
    async with SessionLocal() as db:
        yield DatabaseTransactionService(db=db)


@pytest.fixture(scope="session")
def user_service(transaction):
    return UserService(transaction=transaction)


@pytest.fixture(scope="session")
def hash_service():
    return HashService()


@pytest.fixture(scope="session")
def auth_service(transaction):
    return AuthService(transaction=transaction)


@pytest.fixture(scope="session")
async def create_user(user_service, hash_service):
    users = []

    async def _create_user(email, password, role):
        user = UserCreate(email=email, password=hash_service.hash(password), role=role)
        new_user = await user_service.create_user(user=user)
        users.append(new_user)
        """
            mock is to avoid unexpected mutability of a model
            leading to an update in the database
        """
        user_mock = UserMock(
            id=new_user.id, email=new_user.email, password=password, role=role
        )
        return user_mock

    yield _create_user

    for user in users:
        await user_service.delete_user(user_instance=user)


@pytest.fixture(scope="session")
async def admin_user(create_user) -> Users:
    admin_user = await create_user(
        email="admin@admin.com", password="1234", role="admin"
    )
    return admin_user


@pytest.fixture(scope="session")
async def normal_user(create_user) -> Users:
    normal_user = await create_user(email="user@user.com", password="1234", role="user")
    return normal_user


@pytest.fixture(scope="session")
def access_token(auth_service, admin_user):
    access_token = auth_service.create_token(
        data={"user_id": admin_user.id, "token_type": "access_token"}, expire_minutes=10
    )
    return access_token


@pytest.fixture(scope="session")
def refresh_token(auth_service, admin_user):
    refresh_token = auth_service.create_token(
        data={"user_id": admin_user.id, "token_type": "refresh_token"},
        expire_minutes=10,
    )
    return refresh_token


@pytest.fixture(scope="session", name="client", autouse=True)
async def create_web_client():
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
