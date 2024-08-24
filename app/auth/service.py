from app.config import settings
import jwt
from app.auth.exceptions import AdminUnauthorized, InvalidToken
from app.auth.schemas import TokenCreate, AccessToken
from datetime import datetime, timezone, timedelta
from app.utils.service import HashService
from app.accounts.models import Accounts
from app.auth.constants import TokenType


class AuthService:
    def __init__(
        self,
    ):
        self.JWT_SECRET_KEY = settings.JWT_SECRET_KEY
        self.JWT_ALGORITHM = settings.JWT_ALGORITHM
        self.ACCESS_TOKEN_EXPIRE = settings.ACCESS_TOKEN_EXPIRE
        self.REFRESH_TOKEN_EXPIRE = settings.REFRESH_TOKEN_EXPIRE
        self.hash_service = HashService()

    def _encode(self, to_encode: dict):
        return jwt.encode(to_encode, self.JWT_SECRET_KEY, algorithm=self.JWT_ALGORITHM)

    def _create_token(self, data: dict, expire_minutes: int):
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes=expire_minutes)
        to_encode.update({"exp": expire})
        token = self._encode(to_encode=to_encode)
        return token

    def _decode(self, token):
        try:
            return jwt.decode(token, self.JWT_SECRET_KEY, self.JWT_ALGORITHM)
        except jwt.PyJWTError:
            raise AdminUnauthorized()

    def _verify_token_and_type_for_payload(
        self, token: str, _token_type: TokenType
    ) -> dict:
        payload = self._decode(token=token)
        token_type = payload["token_type"]
        if token_type != _token_type.value:
            raise InvalidToken()
        return payload

    def get_account_id(self, token: str, _token_type: TokenType):
        payload = self._verify_token_and_type_for_payload(
            token=token, _token_type=_token_type
        )
        return payload["id"]

    def verify_account(self, account: Accounts, input_password: str)-> TokenCreate:
        if account is None:
            raise AdminUnauthorized()
        verify = self.hash_service.verify(password=input_password, hashed_password=account.password)
        if not verify:
            raise AdminUnauthorized()
        access_token = self._create_token(
            data={
                "id": account.id,
                "token_type": TokenType.ACCESS_TOKEN.value,
                "type": account.type,
            },
            expire_minutes=self.ACCESS_TOKEN_EXPIRE,
        )
        refresh_token = self._create_token(
            data={
                "id": account.id,
                "token_type": TokenType.REFRESH_TOKEN.value,
                "type": account.type,
            },
            expire_minutes=self.REFRESH_TOKEN_EXPIRE,
        )
        return TokenCreate(access_token=access_token, refresh_token=refresh_token)

    def get_new_access_token_with_refresh_token(self, refresh_token: str) -> AccessToken:
        payload = self._verify_token_and_type_for_payload(
            token=refresh_token, _token_type=TokenType.REFRESH_TOKEN
        )
        account_id = payload["id"]
        account_type = payload["type"]
        access_token = self._create_token(
            data={
                "id": account_id,
                "token_type": TokenType.ACCESS_TOKEN.value,
                "type": account_type,
            },
            expire_minutes=self.ACCESS_TOKEN_EXPIRE,
        )
        return AccessToken(access_token=access_token)
