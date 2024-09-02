from fastapi import APIRouter, Depends, status
from app.business.schemas import (
    BusinessAccountOut,
    BusinessAccountCreate
)
from app.business_user.schemas import BusinessUserAccountCreate, BusinessUserAccountOut, BusinessUserAccountDelete
from app.business.service import BusinessService
from app.tools.schemas import DeleteResponse
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

@business_router.delete(
    "", response_model=DeleteResponse
)
async def delete_business_account(
    business_service: BusinessService = Depends(BusinessService),
    account: Accounts = Depends(get_account),
):
    message = await business_service.delete_business_account(account=account)
    return message

@business_router.get("/me", response_model=BusinessAccountOut)
async def get_business_account_info(
        business_service: BusinessService = Depends(BusinessService),
        account: Accounts = Depends(get_account)):
    business_info = await business_service.get_business_account_info(account=account)
    return business_info

@business_router.post(
    "/add-account",
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
    "/remove-account", response_model=DeleteResponse
)
async def delete_business_user_account(
    business_user: BusinessUserAccountDelete,
    business_service: BusinessService = Depends(BusinessService),
    account: Accounts = Depends(get_account),
):
    message = await business_service.delete_business_user_account(account=account, business_user=business_user)
    return message

