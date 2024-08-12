from passlib.context import CryptContext


class HashService:
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def verify(self, password, hashed_password):
        return self.pwd_context.verify(password, hashed_password)

    def hash(self, password):
        return self.pwd_context.hash(password)
