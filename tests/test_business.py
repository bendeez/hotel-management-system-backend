from app.business.schemas import BusinessAccountCreate, BusinessAccountOut, BusinessUserAccountCreate, BusinessUserAccountOut
from app.business.exceptions import BusinessEmailAlreadyExists
from pydantic import ValidationError
import pytest


def test_business_account_creation(business_service, password, hash_service):
    business_info = BusinessAccountCreate(email="admin@admin.com",
                                          password=password, name="Spa and relax", location="San Francisco")
    business_account = business_service.create_business_account(business=business_info, business_exists=False)
    assert hash_service.verify(password=password, hashed_password=business_account.password)
    assert BusinessAccountOut(id=1,**business_account.__dict__) == BusinessAccountOut(id=1,**business_info.model_dump())

def test_invalid_business_account_creation_through_already_used_email(business_service, password, hash_service):
    business_info = BusinessAccountCreate(email="admin@admin.com",
                                          password=password, name="Spa and relax", location="San Francisco")
    with pytest.raises(BusinessEmailAlreadyExists):
        business_service.create_business_account(business=business_info, business_exists=True)

def test_business_invalid_account_creation_through_missing_fields(business_service, password, hash_service):
    with pytest.raises(ValidationError):
        BusinessAccountCreate(email="admin@admin.com",
                              password=password, name="Spa and relax")  # missing location

def test_business_user_account_creation(business, business_service, password, hash_service):
    _, business = business
    business_user_info = BusinessUserAccountCreate(email="admin@admin.com", password=password, role_name="admin", business_id=business.id)
    business_user_account = business_service.create_business_user_account(account=business, business_user=business_user_info, business_user_exists=False)
    assert hash_service.verify(password=password, hashed_password=business_user_account.password)
    assert BusinessUserAccountOut(id=1, **business_user_account.__dict__) == BusinessUserAccountOut(id=1,
                                                                                       **business_user_info.model_dump())