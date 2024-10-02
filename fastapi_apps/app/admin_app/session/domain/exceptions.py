from app.admin_app.exceptions import AdminError


class SessionsOverflow(AdminError):
    def __init__(
        self,
        message: str = "Too many chat sessions have been requested",
        status_code: int = 400,
    ) -> None:
        super().__init__(message, status_code)


class SessionNotExists(AdminError):
    def __init__(
        self,
        message: str = "Session does not exist",
        status_code: int = 404,
    ) -> None:
        super().__init__(message, status_code)


class SessionExpired(AdminError):
    def __init__(
        self,
        message: str = "Session has expired",
        status_code: int = 404,
    ) -> None:
        super().__init__(message, status_code)


class SessionForbidden(AdminError):
    def __init__(
        self,
        message: str = "The session is not linked to your account",
        status_code: int = 403,
    ) -> None:
        super().__init__(message, status_code)
