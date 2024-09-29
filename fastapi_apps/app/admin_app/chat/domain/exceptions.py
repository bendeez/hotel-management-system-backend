from app.admin_app.exceptions import AdminError


class ChatLogNotFound(AdminError):
    def __init__(
        self,
        message: str = "Chat log not found",
        status_code: int = 404,
    ) -> None:
        super().__init__(message, status_code)
