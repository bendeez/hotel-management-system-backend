from app.admin_app.exceptions import AdminError


class BusinessEmailAlreadyExists(AdminError):
    def __init__(
        self,
        message: str = "Business email already exists",
        status_code: int = 409,
    ) -> None:
        super().__init__(message, status_code)


class BusinessForbidden(AdminError):
    def __init__(
        self,
        message: str = "Your domain cannot perform that action",
        status_code: int = 403,
    ) -> None:
        super().__init__(message, status_code)


class NotABusiness(AdminError):
    def __init__(
        self,
        message: str = "You are not domain",
        status_code: int = 403,
    ) -> None:
        super().__init__(message, status_code)
