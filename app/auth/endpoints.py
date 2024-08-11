from fastapi import APIRouter, Depends, status
from app.auth.schemas import TokenCreate, AccessToken, RefreshToken
from app.user.schemas import UserIn
from app.auth.service import AuthService


auth_router = APIRouter()


@auth_router.post("/login", response_model=TokenCreate)
async def login(user: UserIn, auth_service: AuthService = Depends(AuthService)):
    token = await auth_service.verify_user(user=user)
    return token


@auth_router.post(
    "/refresh", response_model=AccessToken, status_code=status.HTTP_201_CREATED
)
def refresh(token: RefreshToken, auth_service: AuthService = Depends(AuthService)):
    access_token = auth_service.get_new_access_token(refresh_token=token.refresh_token)
    return access_token
