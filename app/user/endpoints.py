from fastapi import APIRouter, Depends
from app.user.schemas import UserAccountOut, UserAccountCreate
from app.user.service import UserService
from app.accounts.models import Accounts
from app.auth.service import get_account


user_router = APIRouter(prefix="/user")


@user_router.post("/", response_model=UserAccountOut)
async def create_user_account(
    user: UserAccountCreate,
    user_service: UserService = Depends(UserService),
    account: Accounts = Depends(get_account),
):
    user_account = user_service.create_user_account(user=user)
    return user_account
