from apps.admin_app.exceptions import AdminError


class UserEmailAlreadyExists(AdminError):
    def __init__(
        self,
        message: str = "User email already exists",
        status_code: int = 409,
    ) -> None:
        super().__init__(message, status_code)


class NotAUser(AdminError):
    def __init__(
        self,
        message: str = "You are not a personal user",
        status_code: int = 409,
    ) -> None:
        super().__init__(message, status_code)
