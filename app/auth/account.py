from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from app.auth.service import AuthService
from app.accounts.repository import AccountsRepository
from app.auth.constants import TokenType

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


async def get_account(
    token: str = Depends(oauth2_scheme),
    auth_service: AuthService = Depends(AuthService),
    account_repository: AccountsRepository = Depends(AccountsRepository),
):
    account_id = auth_service.get_account_id(
        token=token, _token_type=TokenType.ACCESS_TOKEN
    )
    account = await account_repository.get_account_by_id(account_id=account_id)
    return account
