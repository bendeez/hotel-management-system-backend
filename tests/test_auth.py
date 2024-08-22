import pytest
from pytest_lazy_fixtures import lf
from app.auth.schemas import TokenCreate
from app.auth.exceptions import AdminUnauthorized


@pytest.mark.parametrize("account", [lf("user"), lf("business"), lf("business_user")])
def test_login(account, password, auth_service):
    tokens = auth_service.verify_account(account=account, input_password=password)
    assert tokens == TokenCreate(
        access_token=tokens.access_token, refresh_token=tokens.refresh_token
    )


@pytest.mark.parametrize("account", [lf("user"), lf("business"), lf("business_user")])
def test_invalid_password_login(account, auth_service):
    with pytest.raises(AdminUnauthorized):
        auth_service.verify_account(account=account, input_password="wrong password")


def test_account_doesnt_exist(auth_service):
    with pytest.raises(AdminUnauthorized):
        auth_service.verify_account(account=None, input_password="wrong password")


@pytest.mark.parametrize("account", [lf("user"), lf("business"), lf("business_user")])
def test_get_account(account, auth_service):
    pass
