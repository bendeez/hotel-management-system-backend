from fastapi import APIRouter, Depends
from app.user.schemas import UserAccountOut
from app.user.models import Users


user_router = APIRouter(prefix="/user")
