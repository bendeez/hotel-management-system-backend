from fastapi import APIRouter, Depends, status
from app.auth.schemas import TokenCreate, AccessToken, TokenRequest
from app.auth.service import AuthService
from app.business.schemas import BusinessAccountIn, BusinessUserAccountIn
from app.user.schemas import UserAccountIn
from app.accounts.repository import AccountsRepository


auth_router = APIRouter()


@auth_router.post("/login/user", response_model=TokenCreate)
async def user_login(
    user: UserAccountIn,
    account_repository: AccountsRepository = Depends(AccountsRepository),
    auth_service: AuthService = Depends(AuthService),
):
    user_account = await account_repository.get_account_by_email(email=user.email)
    tokens = auth_service.verify_new_account(
        account=user_account, input_password=user.password
    )
    return tokens


@auth_router.post("/login/business", response_model=TokenCreate)
async def business_login(
    business: BusinessAccountIn,
    account_repository: AccountsRepository = Depends(AccountsRepository),
    auth_service: AuthService = Depends(AuthService),
):
    business_account = await account_repository.get_account_by_email(
        email=business.email
    )
    tokens = auth_service.verify_new_account(
        account=business_account, input_password=business.password
    )
    return tokens


@auth_router.post("/login/business-user", response_model=TokenCreate)
async def business_user_login(
    business_user: BusinessUserAccountIn,
    account_repository: AccountsRepository = Depends(AccountsRepository),
    auth_service: AuthService = Depends(AuthService),
):
    account = await account_repository.get_account_by_email(email=business_user.email)
    tokens = auth_service.verify_new_account(
        account=account, input_password=business_user.password
    )
    return tokens


@auth_router.post(
    "/refresh", response_model=AccessToken, status_code=status.HTTP_201_CREATED
)
def refresh(
    token_request: TokenRequest, auth_service: AuthService = Depends(AuthService)
):
    access_token = auth_service.get_new_access_token_with_refresh_token(
        refresh_token=token_request.refresh_token
    )
    return access_token
