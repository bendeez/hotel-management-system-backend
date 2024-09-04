from fastapi import APIRouter, Depends, Request
from app.business_user.service import BusinessUserService
from app.business_user.schemas import BusinessUserAccountOut
from app.accounts.models import Accounts
from app.auth.service import get_account
from app.tools.rate_limiter import limiter, limit

business_user_router = APIRouter()


@business_user_router.get("/business-user/me", response_model=BusinessUserAccountOut)
@limiter.limit(limit)
async def get_business_user_info(
    request: Request,
    business_user_service: BusinessUserService = Depends(BusinessUserService),
    account: Accounts = Depends(get_account),
):
    business_user_info = await business_user_service.get_business_user_account_info(
        account=account
    )
    return business_user_info
