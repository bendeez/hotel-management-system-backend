from fastapi import APIRouter, Depends, status, Request
from apps.admin_app.user.domain.schemas import UserAccountOut, UserAccountCreate
from apps.admin_app.user.domain.service import UserService
from apps.admin_app.user.application.dependencies import get_user_service
from apps.admin_app.accounts.domain.models import Accounts
from apps.admin_app.auth.application.dependencies import get_account
from tools.application.rate_limiter import limiter, limit

user_router = APIRouter()


@user_router.post(
    "/user", response_model=UserAccountOut, status_code=status.HTTP_201_CREATED
)
@limiter.limit(limit)
async def create_user_account(
    request: Request,
    user: UserAccountCreate,
    user_service: UserService = Depends(get_user_service),
):
    user_account = await user_service.create_user_account(user=user)
    return user_account


@user_router.delete("/user", status_code=status.HTTP_204_NO_CONTENT)
@limiter.limit(limit)
async def delete_user_account(
    request: Request,
    user_service: UserService = Depends(get_user_service),
    account: Accounts = Depends(get_account),
):
    await user_service.delete_user_account(account=account)


@user_router.get("/user/me", response_model=UserAccountOut)
@limiter.limit(limit)
async def get_user_account_info(
    request: Request,
    user_service: UserService = Depends(get_user_service),
    account: Accounts = Depends(get_account),
):
    user_info = await user_service.get_user_account_info(account=account)
    return user_info
