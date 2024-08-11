from pydantic import Field
from app.user.schemas import UserAccountCreate
from app.business.schemas import BusinessAccountCreate
from typing import Annotated, Union


AccountCreate = Annotated[Union[UserAccountCreate, BusinessAccountCreate], Field(...,discriminator="account_type")]



