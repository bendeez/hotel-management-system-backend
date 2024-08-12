from app.accounts.enums import AccountType
from pydantic import BaseModel, Field
from app.accounts.schemas import UserAccountIn, BusinessAccountIn, BusinessUserAccountIn
from typing import Annotated, Union


class TokenRequest(BaseModel):
    refresh_token: str
    type: AccountType


class AccessToken(BaseModel):
    access_token: str


class TokenCreate(AccessToken):
    refresh_token: str

LoginInfo = Annotated[Union[UserAccountIn,BusinessAccountIn,BusinessUserAccountIn],Field(...,discriminator="type")]
