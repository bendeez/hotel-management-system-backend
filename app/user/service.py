from app.user.schemas import UserAccountCreate
from app.utils.service import HashService
from app.user.exceptions import UserEmailAlreadyExists
from app.user.models import Users


class UserService:
    def __init__(self):
        self.hash_service = HashService()

    def create_user_account(self, user: UserAccountCreate, user_exists: bool):
        if user_exists:
            raise UserEmailAlreadyExists()
        user.password = self.hash_service.hash(user.password)
        return Users(**user.model_dump())
