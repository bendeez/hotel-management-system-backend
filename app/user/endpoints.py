from fastapi import APIRouter, Depends, status, Request
from app.user.schemas import UserAccountOut, UserAccountCreate
from app.user.service import UserService
from app.accounts.models import Accounts
from app.auth.service import get_account
from app.tools.rate_limiter import limiter, limit

user_router = APIRouter()


@user_router.post(
    "/user", response_model=UserAccountOut, status_code=status.HTTP_201_CREATED
)
@limiter.limit(limit)
async def create_user_account(
    request: Request,
    user: UserAccountCreate,
    user_service: UserService = Depends(UserService),
):
    user_account = await user_service.create_user_account(user=user)
    return user_account


@user_router.delete("/user", status_code=status.HTTP_204_NO_CONTENT)
@limiter.limit(limit)
async def delete_user_account(
    request: Request,
    user_service: UserService = Depends(UserService),
    account: Accounts = Depends(get_account),
):
    await user_service.delete_user_account(account=account)


@user_router.get("/user/me", response_model=UserAccountOut)
@limiter.limit(limit)
async def get_user_account_info(
    request: Request,
    user_service: UserService = Depends(UserService),
    account: Accounts = Depends(get_account),
):
    user_info = await user_service.get_user_account_info(account=account)
    return user_info
