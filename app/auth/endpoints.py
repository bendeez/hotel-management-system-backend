from fastapi import APIRouter, Depends, status
from app.auth.schemas import TokenCreate, AccessToken, TokenRequest, LoginInfo
from app.auth.service import AuthService


auth_router = APIRouter()


@auth_router.post("/login", response_model=TokenCreate)
async def login(
    login_info: LoginInfo, auth_service: AuthService = Depends(AuthService)
):
    tokens = await auth_service.verify_account(login_info=login_info)
    return tokens


@auth_router.post(
    "/refresh", response_model=AccessToken, status_code=status.HTTP_201_CREATED
)
def refresh(
    token_request: TokenRequest, auth_service: AuthService = Depends(AuthService)
):
    access_token = auth_service.get_new_access_token_with_refresh_token(
        refresh_token=token_request.refresh_token,
        account_type=token_request.type,
    )
    return access_token
