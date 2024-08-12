from app.exceptions import AdminError


class BusinessEmailAlreadyExists(AdminError):
    def __init__(
        self,
        message: str = "Business email already exists",
        status_code: int = 409,
    ) -> None:
        super().__init__(message, status_code)
