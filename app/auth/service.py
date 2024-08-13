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
from app.accounts.schemas import UserAccountIn, BusinessAccountIn, BusinessUserAccountIn
from app.accounts.enums import AccountType
from app.accounts.models import Business_Users
from app.user.models import Users
from app.business.models import Business
from app.auth.enums import TokenType
from typing import Union

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
        access_token = self.encode(to_encode=to_encode)
        return access_token

    def decode(self, token):
        return jwt.decode(token, self.JWT_SECRET_KEY, self.JWT_ALGORITHM)

    def verify_token_and_type_for_payload(self, token: str, _token_type: TokenType) -> dict:
        payload = self.decode(token=token)
        token_type = payload.get("token_type")
        if token_type != _token_type.value:
            raise AdminUnauthorized()
        return payload

    def extract_account_id_from_payload(self, payload: dict):
        account_id = payload.get("id")
        if account_id is None:
            raise AdminUnauthorized()
        return account_id

    def verify_account_for_token(
        self,
        input_password: str,
        type: AccountType,
        account: Union[Business_Users, Business, Users, None] = None,
    ) -> TokenCreate:
        if account is None:
            raise AdminUnauthorized()
        verify = self.hash_service.verify(input_password, account.password)
        if not verify:
            raise AdminUnauthorized()
        type = type.value
        access_token = self.create_token(
            data={"id": account.id, "token_type": TokenType.ACCESS_TOKEN.value, "type": type},
            expire_minutes=self.ACCESS_TOKEN_EXPIRE,
        )
        refresh_token = self.create_token(
            data={"id": account.id, "token_type": TokenType.REFRESH_TOKEN.value, "type": type},
            expire_minutes=self.REFRESH_TOKEN_EXPIRE,
        )
        return TokenCreate(access_token=access_token, refresh_token=refresh_token)

    async def verify_business_user(
        self, business_user: BusinessUserAccountIn
    ) -> TokenCreate:
        existing_business_user = (
            await self.account_service.get_business_user_by_username(
                username=business_user.username
            )
        )
        tokens = await self.verify_account_for_token(
            input_password=business_user.password,
            type=AccountType.BUSINESS_USERS,
            account=existing_business_user,
        )
        return tokens

    async def verify_business(self, business: BusinessAccountIn) -> TokenCreate:
        existing_business = await self.account_service.get_business_by_email(
            email=business.email
        )
        tokens = self.verify_account_for_token(
            input_password=business.password,
            type=AccountType.BUSINESS,
            account=existing_business,
        )
        return tokens

    async def verify_user(self, user: UserAccountIn) -> TokenCreate:
        existing_user = await self.account_service.get_user_by_email(email=user.email)
        tokens = self.verify_account_for_token(
            input_password=user.password,
            type=AccountType.USERS,
            account=existing_user,
        )
        return tokens

    async def verify_account(self, login_info: LoginInfo):
        if login_info.type == "users":
            tokens = await self.verify_user(user=login_info)
        elif login_info.type == "business":
            tokens = await self.verify_business(business=login_info)
        elif login_info.type == "business_users":
            tokens = await self.verify_business_user(business_user=login_info)
        else:
            raise AdminUnauthorized()
        return tokens

    def get_new_access_token_with_refresh(self, refresh_token: str, type: AccountType):
        try:
            payload = self.verify_token_and_type_for_payload(
                token=refresh_token, _token_type=TokenType.REFRESH_TOKEN.value
            )
            account_id = self.extract_account_id_from_payload(payload=payload)
            type = type.value
            access_token = self.create_token(
                data={"id": account_id, "token_type": TokenType.ACCESS_TOKEN.value, "type": type},
                expire_minutes=self.ACCESS_TOKEN_EXPIRE,
            )
            return AccessToken(access_token=access_token)
        except jwt.PyJWTError:
            raise InvalidRefreshToken()

    async def decode_access_token_for_account(self, access_token: str) -> Users:
        try:
            payload = self.verify_token_and_type_for_payload(
                token=access_token, _token_type=TokenType.ACCESS_TOKEN.value
            )
            account_id = self.extract_account_id_from_payload(payload=payload)
            type = payload.get("type")
            if type == AccountType.USERS.value:
                account = await self.account_service.get_user_by_id(user_id=account_id)
            elif type == AccountType.BUSINESS.value:
                account = await self.account_service.get_business_by_id(
                    business_id=account_id
                )
            elif type == AccountType.BUSINESS_USERS.value:
                account = await self.account_service.get_business_user_by_id(
                    business_user_id=account_id
                )
            else:
                raise AdminUnauthorized()
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
