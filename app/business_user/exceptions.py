from app.exceptions import AdminError


class BusinessUserEmailAlreadyExists(AdminError):
    def __init__(
        self,
        message: str = "Username already exists within your business user accounts",
        status_code: int = 409,
    ) -> None:
        super().__init__(message, status_code)


class BusinessUserNotFound(AdminError):
    def __init__(
        self,
        message: str = "Business user not found",
        status_code: int = 404,
    ) -> None:
        super().__init__(message, status_code)


class NotABusinessUser(AdminError):
    def __init__(
        self,
        message: str = "You are not a business user",
        status_code: int = 403,
    ) -> None:
        super().__init__(message, status_code)