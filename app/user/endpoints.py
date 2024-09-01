from fastapi import APIRouter, Depends, status
from app.user.schemas import UserAccountOut, UserAccountCreate
from app.user.service import UserService
from app.accounts.models import Accounts
from app.auth.service import get_account


user_router = APIRouter(prefix="/user")


@user_router.post(
    "", response_model=UserAccountOut, status_code=status.HTTP_201_CREATED
)
async def create_user_account(
    user: UserAccountCreate, user_service: UserService = Depends(UserService)
):
    user_account = await user_service.create_user_account(user=user)
    return user_account
