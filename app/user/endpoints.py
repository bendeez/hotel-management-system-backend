from fastapi import APIRouter, Depends
from app.user.schemas import UserAccountOut
from app.auth.service import get_admin_user
from app.user.models import Users


user_router = APIRouter(prefix="/user")


@user_router.get("/me", response_model=UserAccountOut)
async def get_admin_user(admin_user: Users = Depends(get_admin_user)):
    return admin_user
