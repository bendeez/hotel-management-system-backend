from app.exceptions import AdminError


class FacilityNotFound(AdminError):
    def __init__(
        self,
        message: str = "Facility not found",
        status_code: int = 404,
    ) -> None:
        super().__init__(message, status_code)
