from app.tools.db.database import SessionLocal
import asyncio
from app.auth.service import HashService
from app.user.schemas import UserCreate
from app.tools.db.database_transaction import DatabaseTransactionService
from app.user.service import UserService


async def main():
    async with SessionLocal() as db:
        hash_service = HashService()
        user_service = UserService(transaction=DatabaseTransactionService(db=db))
        while True:
            email = input("Email: ")
            password = input("Password: ")
            role = input("Role: ")
            user = UserCreate(
                email=email, password=hash_service.hash(password), role=role
            )
            new_user = await user_service.create_user(user=user)
            print(new_user.__dict__)
            print("Admin user have been create successfully")


asyncio.run(main())
