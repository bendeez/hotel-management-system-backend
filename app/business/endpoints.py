from fastapi import APIRouter, Depends, status
from app.business.schemas import (
    BusinessAccountOut,
    BusinessAccountCreate,
)
from app.business_user.schemas import BusinessUserAccountCreate, BusinessUserAccountOut
from app.business.service import BusinessService
from app.auth.service import get_account
from app.accounts.models import Accounts


business_router = APIRouter(prefix="/business")


@business_router.post(
    "", response_model=BusinessAccountOut, status_code=status.HTTP_201_CREATED
)
async def create_business_account(
    business: BusinessAccountCreate,
    business_service: BusinessService = Depends(BusinessService),
):
    business_account = await business_service.create_business_account(business=business)
    return business_account


@business_router.post(
    "/add-user",
    response_model=BusinessUserAccountOut,
    status_code=status.HTTP_201_CREATED,
)
async def add_account_to_business(
    business_user: BusinessUserAccountCreate,
    account: Accounts = Depends(get_account),
    business_service: BusinessService = Depends(BusinessService),
):
    business_user_account = await business_service.create_business_user_account(
        account=account,
        business_user=business_user,
    )
    return business_user_account
