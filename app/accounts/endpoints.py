from fastapi import APIRouter, Depends
from app.accounts.service import AccountsService
from app.accounts.schemas import (
    UserAccountCreate,
    BusinessAccountCreate,
    BusinessUserAccountCreate,
    BusinessAccountOut,
    UserAccountOut,
    BusinessUserAccountOut
)

account_router = APIRouter(prefix="/account")


@account_router.post("/user", response_model=UserAccountOut)
async def create_user_account(
    user: UserAccountCreate, account_service: AccountsService = Depends(AccountsService)
):
    user_account = await account_service.create_user_account(user=user)
    return user_account


@account_router.post("/business", response_model=BusinessAccountOut)
async def create_business_account(
    business: BusinessAccountCreate,
    account_service: AccountsService = Depends(AccountsService),
):
    business_account = await account_service.create_business_account(business=business)
    return business_account


@account_router.post("/business-user", response_model=BusinessUserAccountOut)
async def create_business_user_account(
    business_user: BusinessUserAccountCreate,
    account_service: AccountsService = Depends(AccountsService),
):
    business_user_account = await account_service.create_business_user_account(
        business_user=business_user
    )
    return business_user_account
