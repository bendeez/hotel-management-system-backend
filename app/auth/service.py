from app.config import settings
import jwt
from fastapi.security import OAuth2PasswordBearer
from app.auth.exceptions import AdminUnauthorized, InvalidRefreshToken
from app.auth.schemas import TokenCreate, LoginInfo
from datetime import datetime, timezone, timedelta
from fastapi import Depends
from app.tools.db.database_transaction import DatabaseTransactionService
from app.auth.schemas import AccessToken
from app.tools.base_service import BaseService
from app.utils.service import HashService
from app.accounts.service import AccountsService
from app.accounts.enums import AccountType
from app.user.models import Users
from app.auth.enums import TokenType
from app.tools.enums import get_enum_by_value

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


class AuthService(BaseService):
    def __init__(
        self,
        transaction: DatabaseTransactionService = Depends(DatabaseTransactionService),
    ):
        super().__init__(transaction=transaction)
        self.JWT_SECRET_KEY = settings.JWT_SECRET_KEY
        self.JWT_ALGORITHM = settings.JWT_ALGORITHM
        self.ACCESS_TOKEN_EXPIRE = settings.ACCESS_TOKEN_EXPIRE
        self.REFRESH_TOKEN_EXPIRE = settings.REFRESH_TOKEN_EXPIRE
        self.hash_service = HashService()
        self.account_service = AccountsService(transaction=self.transaction)

    def encode(self, to_encode: dict):
        return jwt.encode(to_encode, self.JWT_SECRET_KEY, algorithm=self.JWT_ALGORITHM)

    def create_token(self, data: dict, expire_minutes: int):
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes=expire_minutes)
        to_encode.update({"exp": expire})
        token = self.encode(to_encode=to_encode)
        return token

    def decode(self, token):
        return jwt.decode(token, self.JWT_SECRET_KEY, self.JWT_ALGORITHM)

    def verify_token_and_type_for_payload(self, token: str, _token_type: TokenType) -> dict:
        payload = self.decode(token=token)
        token_type = payload["token_type"]
        if token_type != _token_type.value:
            raise AdminUnauthorized()
        return payload

    async def verify_account(self, login_info: LoginInfo):
        account = await self.account_service.get_account_by_email(account_type=login_info.type, email=login_info.email)
        if account is None:
            raise AdminUnauthorized()
        verify = self.hash_service.verify(login_info.password, account.password)
        if not verify:
            raise AdminUnauthorized()
        access_token = self.create_token(
            data={"id": account.id, "token_type": TokenType.ACCESS_TOKEN.value, "type": login_info.type.value},
            expire_minutes=self.ACCESS_TOKEN_EXPIRE,
        )
        refresh_token = self.create_token(
            data={"id": account.id, "token_type": TokenType.REFRESH_TOKEN.value, "type": login_info.type.value},
            expire_minutes=self.REFRESH_TOKEN_EXPIRE,
        )
        return TokenCreate(access_token=access_token, refresh_token=refresh_token)

    def get_new_access_token_with_refresh_token(self, refresh_token: str, account_type: AccountType):
        try:
            payload = self.verify_token_and_type_for_payload(
                token=refresh_token, _token_type=TokenType.REFRESH_TOKEN
            )
            account_id = payload["id"]
            access_token = self.create_token(
                data={"id": account_id, "token_type": TokenType.ACCESS_TOKEN.value, "type": account_type.value},
                expire_minutes=self.ACCESS_TOKEN_EXPIRE,
            )
            return AccessToken(access_token=access_token)
        except jwt.PyJWTError:
            raise InvalidRefreshToken()

    async def decode_access_token_for_account(self, access_token: str) -> Users:
        try:
            payload = self.verify_token_and_type_for_payload(
                token=access_token, _token_type=TokenType.ACCESS_TOKEN
            )
            account_id = payload["id"]
            account_type = get_enum_by_value(enum=AccountType, value=payload["type"])
            account = await self.account_service.get_account_by_id(account_type=account_type, id=account_id)
            if account is None:
                raise AdminUnauthorized()
            return account
        except jwt.PyJWTError:
            raise AdminUnauthorized()


async def get_account(
    token: str = Depends(oauth2_scheme),
    auth_service: AuthService = Depends(AuthService),
):
    account = await auth_service.decode_access_token_for_account(access_token=token)
    return account
