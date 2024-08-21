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
    payload = auth_service.verify_token_and_type_for_payload(
        token=token, _token_type=TokenType.ACCESS_TOKEN
    )
    account_id = payload["id"]
    account = await account_repository.get_account_by_id(account_id=account_id)
    return account
