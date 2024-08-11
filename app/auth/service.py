from app.config import settings
import jwt
from fastapi.security import OAuth2PasswordBearer
from app.auth.exceptions import AdminUnauthorized, InvalidRefreshToken
from app.auth.schemas import TokenCreate
from app.user.schemas import UserIn
from datetime import datetime, timezone, timedelta
from fastapi import Depends
from app.user.models import Users
from passlib.context import CryptContext
from app.tools.db.database_transaction import DatabaseTransactionService
from app.auth.schemas import AccessToken
from app.tools.base_service import BaseService
from app.user.service import UserService


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


class HashService:
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def verify(self, password, hashed_password):
        return self.pwd_context.verify(password, hashed_password)

    def hash(self, password):
        return self.pwd_context.hash(password)


class AuthService(BaseService):
    def __init__(self, transaction=Depends(DatabaseTransactionService)):
        super().__init__()
        self.JWT_SECRET_KEY = settings.JWT_SECRET_KEY
        self.JWT_ALGORITHM = settings.JWT_ALGORITHM
        self.ACCESS_TOKEN_EXPIRE = settings.ACCESS_TOKEN_EXPIRE
        self.REFRESH_TOKEN_EXPIRE = settings.REFRESH_TOKEN_EXPIRE
        self.hash_service = HashService()
        self.transaction = transaction
        self.user_service = UserService(transaction=transaction)

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

    async def verify_user(self, user: UserIn) -> TokenCreate:
        existing_user = await self.user_service.get_user_by_email(email=user.email)
        if existing_user is None:
            raise AdminUnauthorized()
        if existing_user.role != "admin":
            raise AdminUnauthorized()
        verify = self.hash_service.verify(user.password, existing_user.password)
        if not verify:
            raise AdminUnauthorized()
        access_token = self.create_token(
            data={"user_id": existing_user.id, "token_type": "access_token"},
            expire_minutes=self.ACCESS_TOKEN_EXPIRE,
        )
        refresh_token = self.create_token(
            data={"user_id": existing_user.id, "token_type": "refresh_token"},
            expire_minutes=self.REFRESH_TOKEN_EXPIRE,
        )
        return TokenCreate(access_token=access_token, refresh_token=refresh_token)

    def get_new_access_token(self, refresh_token: str):
        try:
            payload = self.decode(token=refresh_token)
            token_type = payload.get("token_type")
            if token_type != "refresh_token":
                raise InvalidRefreshToken()
            user_id = payload.get("user_id")
            if user_id is None:
                raise InvalidRefreshToken()
            access_token = self.create_token(
                data={"user_id": user_id, "token_type": "access_token"},
                expire_minutes=self.ACCESS_TOKEN_EXPIRE,
            )
            return AccessToken(access_token=access_token)
        except jwt.PyJWTError:
            raise InvalidRefreshToken()

    async def decode_access_token(self, access_token: str) -> Users:
        try:
            payload = self.decode(token=access_token)
            token_type = payload.get("token_type")
            if token_type != "access_token":
                raise AdminUnauthorized()
            user_id = payload.get("user_id")
            if user_id is None:
                raise AdminUnauthorized()
            user = await self.user_service.get_user_by_id(user_id=user_id)
            if user is None:
                raise AdminUnauthorized()
            if user.role != "admin":
                raise AdminUnauthorized()
            return user
        except jwt.PyJWTError:
            raise AdminUnauthorized()


async def get_admin_user(
    token: str = Depends(oauth2_scheme),
    auth_service: AuthService = Depends(AuthService),
):
    admin_user = await auth_service.decode_access_token(access_token=token)
    return admin_user
