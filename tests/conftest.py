from app.user.models import Users
from app.business.models import Business, Business_Users
from app.auth.service import AuthService
from app.utils.service import HashService
from pytest_lazy_fixtures import lf
import pytest


@pytest.fixture(scope="session")
def auth_service():
    return AuthService()


@pytest.fixture(scope="session")
def hash_service():
    return HashService()


@pytest.fixture(scope="session")
def password():
    return "1234"


@pytest.fixture(scope="session")
def hashed_password(password, hash_service):
    return hash_service.hash(password)


@pytest.fixture(scope="session")
def user(hashed_password) -> Users:
    return Users(id=1, email="user@gmail.com", password=hashed_password)


@pytest.fixture(scope="session")
def business(hashed_password) -> Business:
    return Business(id=2, email="user@gmail.com", password=hashed_password)


@pytest.fixture(scope="session")
def business_user(hashed_password) -> Business_Users:
    return Business_Users(
        id=3, email="user@gmail.com", password=hashed_password, business_id=2
    )


@pytest.fixture(
    scope="session", params=[lf("user"), lf("business"), lf("business_user")]
)
def access_tokens(request):
    account = request.param
