from app.exceptions import AdminError


class BusinessForbidden(AdminError):
    def __init__(
        self,
        message: str = "Your business cannot perform that action",
        status_code: int = 403,
    ) -> None:
        super().__init__(message, status_code)

class BusinessUserUsernameAlreadyExists(AdminError):
    def __init__(
        self,
        message: str = "Username already exists within your business user accounts",
        status_code: int = 409,
    ) -> None:
        super().__init__(message, status_code)