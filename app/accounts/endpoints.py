from fastapi import APIRouter, Depends
from app.accounts.service import AccountsService
from app.accounts.schemas import AccountCreate, Account
from app.accounts.schemas import (
    UserAccountOut,
    BusinessAccountOut,
    BusinessUserAccountCreate,
    BusinessUserAccountOut,
)
from typing import Union
from app.auth.service import get_account

account_router = APIRouter(prefix="/account")


@account_router.post("/", response_model=Union[UserAccountOut, BusinessAccountOut])
async def create_user_account(
    account: AccountCreate, account_service: AccountsService = Depends(AccountsService)
):
    account = await account_service.create_account(account=account)
    return account


@account_router.post("/add", response_model=BusinessUserAccountOut)
async def add_account_to_business(
    business_user: BusinessUserAccountCreate,
    account: Account = Depends(get_account),
    account_service: AccountsService = Depends(AccountsService),
):
    business_user_account = await account_service.create_business_user_account(
        account=account, business_user=business_user
    )
    return business_user_account
