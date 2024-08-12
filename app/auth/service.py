from app.config import settings
import jwt
from fastapi.security import OAuth2PasswordBearer
from app.auth.exceptions import AdminUnauthorized, InvalidRefreshToken
from app.auth.schemas import TokenCreate
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
from app.auth.enums import PayloadKey
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

    def verify_token_and_type_for_account_id(
        self, token: str, _token_type: str, account_type: AccountType
    ) -> int:
        payload = self.decode(token=token)
        token_type = payload.get("token_type")
        if token_type != _token_type:
            raise AdminUnauthorized()
        account_type = account_type.value
        payload_key = getattr(PayloadKey, account_type).value
        account_id = payload.get(payload_key)
        if account_id is None:
            raise AdminUnauthorized()
        return account_id

    def verify_account_for_token(
        self,
        input_password: str,
        account_type: AccountType,
        account: Union[Business_Users, Business, Users, None] = None,
    ) -> TokenCreate:
        if account is None:
            raise AdminUnauthorized()
        verify = self.hash_service.verify(input_password, account.password)
        if not verify:
            raise AdminUnauthorized()
        account_type = account_type.value
        account_key = getattr(PayloadKey, account_type).value
        access_token = self.create_token(
            data={account_key: account.id, "token_type": "access_token"},
            expire_minutes=self.ACCESS_TOKEN_EXPIRE,
        )
        refresh_token = self.create_token(
            data={account_key: account.id, "token_type": "refresh_token"},
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
            account_type=AccountType.BUSINESS_USERS,
            account=existing_business_user,
        )
        return tokens

    async def verify_business(self, business: BusinessAccountIn) -> TokenCreate:
        existing_business = await self.account_service.get_business_by_email(
            email=business.email
        )
        tokens = await self.verify_account_for_token(
            input_password=business.password,
            account_type=AccountType.BUSINESS,
            account=existing_business,
        )
        return tokens

    async def verify_user(self, user: UserAccountIn) -> TokenCreate:
        existing_user = await self.account_service.get_user_by_email(email=user.email)
        tokens = self.verify_account_for_token(
            input_password=user.password,
            account_type=AccountType.USERS,
            account=existing_user,
        )
        return tokens

    def get_new_access_token_with_refresh(
        self, refresh_token: str, account_type: AccountType
    ):
        try:
            account_id = self.verify_token_and_type_for_account_id(
                token=refresh_token,
                _token_type="refresh_token",
                account_type=account_type,
            )
            account_type = account_type.value
            account_key = getattr(PayloadKey, account_type).value
            access_token = self.create_token(
                data={account_key: account_id, "token_type": "access_token"},
                expire_minutes=self.ACCESS_TOKEN_EXPIRE,
            )
            return AccessToken(access_token=access_token)
        except jwt.PyJWTError:
            raise InvalidRefreshToken()

    async def decode_access_token_for_account(
        self, access_token: str, account_type: AccountType
    ) -> Users:
        try:
            account_id = self.verify_token_and_type_for_account_id(
                token=access_token,
                _token_type="access_token",
                account_type=account_type,
            )
            account_type = account_type.value
            if account_type == "users":
                account = await self.account_service.get_user_by_id(user_id=account_id)
            elif account_type == "business":
                account = await self.account_service.get_business_by_id(
                    business_id=account_id
                )
            else:
                account = await self.account_service.get_business_user_by_id(
                    business_user_id=account_id
                )
            if account is None:
                raise AdminUnauthorized()
            return account
        except jwt.PyJWTError:
            raise AdminUnauthorized()


async def get_user_account(
    token: str = Depends(oauth2_scheme),
    auth_service: AuthService = Depends(AuthService),
):
    user_account = await auth_service.decode_access_token_for_account(
        access_token=token, account_type=AccountType.USERS
    )
    return user_account


async def get_business_account(
    token: str = Depends(oauth2_scheme),
    auth_service: AuthService = Depends(AuthService),
):
    business_account = await auth_service.decode_access_token_for_account(
        access_token=token, account_type=AccountType.BUSINESS
    )
    return business_account


async def get_business_user_account(
    token: str = Depends(oauth2_scheme),
    auth_service: AuthService = Depends(AuthService),
):
    business_user_account = await auth_service.decode_access_token_for_account(
        access_token=token, account_type=AccountType.BUSINESS_USERS
    )
    return business_user_account
