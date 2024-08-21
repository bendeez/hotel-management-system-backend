from fastapi import APIRouter, Depends
from app.business.schemas import (
    BusinessAccountOut,
    BusinessAccountCreate,
    BusinessUserAccountCreate,
    BusinessUserAccountOut,
)
from app.business.repository import BusinessRepository
from app.business.service import BusinessService
from app.auth.account import get_account
from app.accounts.models import Accounts

business_router = APIRouter(prefix="/business")


@business_router.post("/", response_model=BusinessAccountOut)
async def create_business_account(
    business: BusinessAccountCreate,
    business_repository: BusinessRepository = Depends(BusinessRepository),
    business_service: BusinessService = Depends(BusinessService),
):
    existing_business = await business_repository.get_business_by_email(
        email=business.email
    )
    if existing_business is None:
        business_exists = False
    else:
        business_exists = True
    business_account = business_service.create_business_account(
        business=business, business_exists=business_exists
    )
    saved_business_account = await business_repository.create(business_account)
    return saved_business_account


@business_router.post("/add", response_model=BusinessUserAccountOut)
async def add_account_to_business(
    business_user: BusinessUserAccountCreate,
    account: Accounts = Depends(get_account),
    business_repository: BusinessRepository = Depends(BusinessRepository),
    business_service: BusinessService = Depends(BusinessService),
):
    existing_business_user = await business_repository.get_business_user_by_email(
        email=business_user.email
    )
    if existing_business_user is None:
        business_user_exists = False
    else:
        business_user_exists = True
    business_user_account = business_service.create_business_user_account(
        account=account,
        business_user=business_user,
        business_user_exists=business_user_exists,
    )
    saved_business_user_account = await business_repository.create(
        business_user_account
    )
    return saved_business_user_account
