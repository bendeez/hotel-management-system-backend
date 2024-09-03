from fastapi import APIRouter, Depends, status
from app.business.schemas import BusinessAccountOut, BusinessAccountCreate
from app.business_user.schemas import (
    BusinessUserAccountCreate,
    BusinessUserAccountOut,
)
from app.business.service import BusinessService
from app.auth.service import get_account
from app.accounts.models import Accounts


business_router = APIRouter()


@business_router.post(
    "/business", response_model=BusinessAccountOut, status_code=status.HTTP_201_CREATED
)
async def create_business_account(
    business: BusinessAccountCreate,
    business_service: BusinessService = Depends(BusinessService),
):
    business_account = await business_service.create_business_account(business=business)
    return business_account


@business_router.delete("/business", status_code=status.HTTP_204_NO_CONTENT)
async def delete_business_account(
    business_service: BusinessService = Depends(BusinessService),
    account: Accounts = Depends(get_account),
):
    await business_service.delete_business_account(account=account)


@business_router.get("/business/me", response_model=BusinessAccountOut)
async def get_business_account_info(
    business_service: BusinessService = Depends(BusinessService),
    account: Accounts = Depends(get_account),
):
    business_info = await business_service.get_business_account_info(account=account)
    return business_info


@business_router.post(
    "/business/add-account",
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


@business_router.delete(
    "/business/remove-account/{business_user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_business_user_account(
    business_user_id: int,
    business_service: BusinessService = Depends(BusinessService),
    account: Accounts = Depends(get_account),
):
    await business_service.delete_business_user_account(
        account=account, business_user_id=business_user_id
    )
