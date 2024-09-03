from fastapi import APIRouter, Depends
from app.business_user.service import BusinessUserService
from app.business_user.schemas import BusinessUserAccountOut
from app.accounts.models import Accounts
from app.auth.service import get_account

business_user_router = APIRouter()


@business_user_router.get("/business-user/me", response_model=BusinessUserAccountOut)
async def get_business_user_info(
    business_user_service: BusinessUserService = Depends(BusinessUserService),
    account: Accounts = Depends(get_account),
):
    business_user_info = await business_user_service.get_business_user_account_info(
        account=account
    )
    return business_user_info
