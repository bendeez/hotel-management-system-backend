import pytest
from pytest_lazy_fixtures import lf
from app.auth.schemas import TokenCreate, AccessToken
from app.auth.exceptions import AdminUnauthorized, InvalidToken
from app.auth.constants import TokenType


@pytest.mark.parametrize("account", [lf("user"), lf("business"), lf("business_user")])
def test_login(account, password, auth_service):
    _, account = account
    tokens = auth_service.verify_account(account=account, input_password=password)
    assert tokens == TokenCreate(
        access_token=tokens.access_token, refresh_token=tokens.refresh_token
    )


@pytest.mark.parametrize("account", [lf("user"), lf("business"), lf("business_user")])
def test_invalid_password_login(account, auth_service):
    _, account = account
    with pytest.raises(AdminUnauthorized):
        auth_service.verify_account(account=account, input_password="wrong password")


def test_account_doesnt_exist(auth_service):
    with pytest.raises(AdminUnauthorized):
        auth_service.verify_account(account=None, input_password="wrong password")


@pytest.mark.parametrize("account", [lf("user"), lf("business"), lf("business_user")])
def test_get_account(account, auth_service):
    tokens, account = account
    account_id = auth_service.get_account_id(
        token=tokens.access_token, _token_type=TokenType.ACCESS_TOKEN
    )
    assert account_id == account.id


def test_invalid_get_account(auth_service):
    with pytest.raises(AdminUnauthorized):
        auth_service.get_account_id(
            token="485657375467", _token_type=TokenType.ACCESS_TOKEN
        )


@pytest.mark.parametrize("account", [lf("user"), lf("business"), lf("business_user")])
def test_get_access_token_with_refresh_token(account, auth_service):
    tokens, _ = account
    access_token = auth_service.get_new_access_token_with_refresh_token(
        refresh_token=tokens.refresh_token
    )
    assert access_token == AccessToken(access_token=access_token.access_token)


@pytest.mark.parametrize("account", [lf("user"), lf("business"), lf("business_user")])
def test_invalid_get_access_token_with_access_token(account, auth_service):
    tokens, _ = account
    with pytest.raises(InvalidToken):
        auth_service.get_new_access_token_with_refresh_token(
            refresh_token=tokens.access_token
        )
