from fastapi import APIRouter, Depends, status
from app.auth.schemas import TokenCreate, AccessToken, TokenRequest
from app.accounts.schemas import UserAccountIn, BusinessAccountIn, BusinessUserAccountIn
from app.auth.service import AuthService


auth_router = APIRouter(prefix="/login")


@auth_router.post("/user", response_model=TokenCreate)
async def login_user(
    user: UserAccountIn, auth_service: AuthService = Depends(AuthService)
):
    token = await auth_service.verify_user(user=user)
    return token


@auth_router.post("/business", response_model=TokenCreate)
async def login_business(
    business: BusinessAccountIn, auth_service: AuthService = Depends(AuthService)
):
    token = await auth_service.verify_business(business=business)
    return token


@auth_router.post("/business-user", response_model=TokenCreate)
async def login_business(
    business_user: BusinessUserAccountIn,
    auth_service: AuthService = Depends(AuthService),
):
    token = await auth_service.verify_business_user(business_user=business_user)
    return token


@auth_router.post(
    "/refresh", response_model=AccessToken, status_code=status.HTTP_201_CREATED
)
def refresh(
    token_request: TokenRequest, auth_service: AuthService = Depends(AuthService)
):
    access_token = auth_service.get_new_access_token_with_refresh(
        refresh_token=token_request.refresh_token,
        account_type=token_request.account_type,
    )
    return access_token
