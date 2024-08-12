from app.exceptions import AdminError


class BusinessForbidden(AdminError):
    def __init__(
        self, message: str = "Your business cannot perform that action", status_code: int = 401
    ) -> None:
        super().__init__(message, status_code)
