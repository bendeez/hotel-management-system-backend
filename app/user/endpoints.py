from fastapi import APIRouter, Depends
from app.user.schemas import UserAccountOut, UserAccountCreate
from app.user.service import UserService
from app.user.repository import UserRepository


user_router = APIRouter(prefix="/user")


@user_router.post("/", response_model=UserAccountOut)
async def create_user_account(
    user: UserAccountCreate,
    user_repository: UserRepository = Depends(UserRepository),
    user_service: UserService = Depends(UserService),
):
    existing_user = await user_repository.get_user_by_email(email=user.email)
    if existing_user is None:
        user_exists = False
    else:
        user_exists = True
    user_account = user_service.create_user_account(user=user, user_exists=user_exists)
    saved_user_account = await user_repository.create(user_account)
    return saved_user_account
