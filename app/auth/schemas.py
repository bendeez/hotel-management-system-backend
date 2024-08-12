from pydantic import BaseModel
from app.accounts.enums import AccountType


class TokenRequest(BaseModel):
    refresh_token: str
    account_type: AccountType


class AccessToken(BaseModel):
    access_token: str


class TokenCreate(AccessToken):
    refresh_token: str
