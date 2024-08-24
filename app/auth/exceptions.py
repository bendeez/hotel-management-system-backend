from app.exceptions import AdminError


class AdminUnauthorized(AdminError):
    def __init__(
        self, message: str = "Invalid credentials", status_code: int = 401
    ) -> None:
        super().__init__(message, status_code)

class InvalidToken(AdminError):
    def __init__(
        self, message: str = "Invalid token", status_code: int = 409
    ) -> None:
        super().__init__(message, status_code)

