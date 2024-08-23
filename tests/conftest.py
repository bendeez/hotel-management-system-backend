from app.user.models import Users
from app.user.schemas import UserAccountIn
from app.business.models import Business, Business_Users
from app.business.schemas import BusinessAccountCreate, BusinessUserAccountCreate
from app.auth.service import AuthService
from app.auth.schemas import TokenCreate
from app.utils.service import HashService
from app.business.service import BusinessService
import pytest


@pytest.fixture(scope="session")
def auth_service():
    return AuthService()


@pytest.fixture(scope="session")
def hash_service():
    return HashService()

@pytest.fixture(scope="session")
def business_service():
    return BusinessService()


@pytest.fixture(scope="session")
def password():
    return "1234"


@pytest.fixture(scope="session")
def hashed_password(password, hash_service):
    return hash_service.hash(password)


@pytest.fixture(scope="session")
def user(hashed_password, password, auth_service) -> tuple[TokenCreate,Users]:
    user = Users(**UserAccountIn(id=1, email="user@gmail.com", password=hashed_password).model_dump())
    tokens = auth_service.verify_account(account=user, input_password=password)
    return tokens, user

@pytest.fixture(scope="session")
def business(hashed_password, password, auth_service) -> tuple[TokenCreate,Business]:
    business = Business(id=2, **BusinessAccountCreate(email="admin@admin.com",
                        password=hashed_password, name="Spa and relax", location="San Francisco").model_dump())
    tokens = auth_service.verify_account(account=business, input_password=password)
    return tokens, business

@pytest.fixture(scope="session")
def business_user(hashed_password, password, auth_service) -> tuple[TokenCreate,Business_Users]:
    business_user = Business_Users(
        id=3, **BusinessUserAccountCreate(email="user@gmail.com", password=hashed_password, business_id=2, role_name="admin").model_dump()
    )
    tokens = auth_service.verify_account(account=business_user, input_password=password)
    return tokens, business_user


