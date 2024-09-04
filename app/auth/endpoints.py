from fastapi import APIRouter, Depends, status, Request
from app.auth.schemas import TokenCreate, AccessToken, TokenRequest
from app.auth.service import AuthService
from app.business.schemas import BusinessAccountIn
from app.business_user.schemas import BusinessUserAccountIn
from app.user.schemas import UserAccountIn
from app.tools.rate_limiter import limiter, limit


auth_router = APIRouter()


@auth_router.post("/login/user", response_model=TokenCreate)
@limiter.limit(limit)
async def user_login(
    request: Request,
    user: UserAccountIn,
    auth_service: AuthService = Depends(AuthService),
):
    tokens = await auth_service.verify_account(
        email=user.email, input_password=user.password
    )
    return tokens


@auth_router.post("/login/business", response_model=TokenCreate)
@limiter.limit(limit)
async def business_login(
    request: Request,
    business: BusinessAccountIn,
    auth_service: AuthService = Depends(AuthService),
):
    tokens = await auth_service.verify_account(
        email=business.email, input_password=business.password
    )
    return tokens


@auth_router.post("/login/business-user", response_model=TokenCreate)
@limiter.limit(limit)
async def business_user_login(
    request: Request,
    business_user: BusinessUserAccountIn,
    auth_service: AuthService = Depends(AuthService),
):
    tokens = await auth_service.verify_account(
        email=business_user.email, input_password=business_user.password
    )
    return tokens


@auth_router.post(
    "/refresh", response_model=AccessToken, status_code=status.HTTP_201_CREATED
)
@limiter.limit(limit)
def refresh(
    request: Request,
    token_request: TokenRequest,
    auth_service: AuthService = Depends(AuthService),
):
    access_token = auth_service.get_new_access_token_with_refresh_token(
        refresh_token=token_request.refresh_token
    )
    return access_token
