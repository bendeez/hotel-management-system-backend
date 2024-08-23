from app.user.schemas import UserAccountOut, UserAccountCreate
import pytest
from app.user.exceptions import UserEmailAlreadyExists
from pydantic import ValidationError

def test_user_account_creation(user_service, hash_service, password):
    user_info = UserAccountCreate(email="admin@admin.com",
                                          password=password)
    user_account = user_service.create_user_account(user=user_info, user_email_exists=False)
    assert hash_service.verify(password=password, hashed_password=user_account.password)
    assert UserAccountOut(id=1, **user_account.__dict__) == UserAccountOut(id=1, **user_info.model_dump())

def test_invalid_user_account_creation_through_already_used_email(user_service, password):
    user_info = UserAccountCreate(email="admin@admin.com",
                              password=password)
    with pytest.raises(UserEmailAlreadyExists):
        user_service.create_user_account(user=user_info, user_email_exists=True)

def test_invalid_user_account_creation_through_missing_fields(business_service, password, hash_service):
    with pytest.raises(ValidationError):
        UserAccountCreate(email="admin@admin.com")  # missing password
