from app.user.models import Users
from app.business.models import Business
from enum import Enum

class AccountMapper(Enum):
    user = Users
    business = Business