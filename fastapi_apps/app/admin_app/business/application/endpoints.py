from fastapi import APIRouter, Depends, status, Request
from app.admin_app.business.domain.schemas import (
    BusinessAccountOut,
    BusinessAccountCreate,
)
from app.admin_app.business_user.domain.schemas import (
    BusinessUserAccountCreate,
    BusinessUserAccountOut,
)
from app.admin_app.business.domain.service import BusinessService
from app.admin_app.auth.application.dependencies import get_account
from app.admin_app.accounts.domain.models import Accounts
from app.tools.application.rate_limiter import limiter, limit
from app.admin_app.business.application.dependencies import get_business_service


business_router = APIRouter()


@business_router.post(
    "/business", response_model=BusinessAccountOut, status_code=status.HTTP_201_CREATED
)
@limiter.limit(limit)
async def create_business_account(
    request: Request,
    business: BusinessAccountCreate,
    business_service: BusinessService = Depends(get_business_service),
):
    business_account = await business_service.create_business_account(business=business)
    return business_account


@business_router.delete("/business", status_code=status.HTTP_204_NO_CONTENT)
@limiter.limit(limit)
async def delete_business_account(
    request: Request,
    business_service: BusinessService = Depends(get_business_service),
    account: Accounts = Depends(get_account),
):
    await business_service.delete_business_account(account=account)


@business_router.get("/business/me", response_model=BusinessAccountOut)
@limiter.limit(limit)
async def get_business_account_info(
    request: Request,
    business_service: BusinessService = Depends(get_business_service),
    account: Accounts = Depends(get_account),
):
    business_info = await business_service.get_business_account_info(account=account)
    return business_info


@business_router.post(
    "/business/add-account",
    response_model=BusinessUserAccountOut,
    status_code=status.HTTP_201_CREATED,
)
@limiter.limit(limit)
async def add_account_to_business(
    request: Request,
    business_user: BusinessUserAccountCreate,
    account: Accounts = Depends(get_account),
    business_service: BusinessService = Depends(get_business_service),
):
    business_user_account = await business_service.create_business_user_account(
        account=account,
        business_user=business_user,
    )
    return business_user_account


@business_router.delete(
    "/business/remove-account/{business_user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
@limiter.limit(limit)
async def delete_business_user_account(
    request: Request,
    business_user_id: int,
    business_service: BusinessService = Depends(get_business_service),
    account: Accounts = Depends(get_account),
):
    await business_service.delete_business_user_account(
        account=account, business_user_id=business_user_id
    )
