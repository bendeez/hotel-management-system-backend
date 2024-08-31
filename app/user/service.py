from fastapi import Depends
from app.user.schemas import UserAccountCreate
from app.utils.service import HashService
from app.user.exceptions import UserEmailAlreadyExists
from app.user.models import Users
from app.user.repository import UserRepository


class UserService:
    def __init__(self, repository: UserRepository = Depends(UserRepository)):
        self.hash_service = HashService()
        self.repository = repository

    async def create_user_account(self, user: UserAccountCreate):
        existing_user = await self.repository.get_user_by_email(email=user.email)
        if existing_user is not None:
            raise UserEmailAlreadyExists()
        user.password = self.hash_service.hash(user.password)
        user_account = await self.repository.create(Users(**user.model_dump()))
        return user_account
