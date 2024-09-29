from app.admin_app.exceptions import AdminError
from app.admin_app.auth.domain.constants import TokenType


class AdminUnauthorized(AdminError):
    def __init__(
        self, message: str = "Invalid credentials", status_code: int = 401
    ) -> None:
        super().__init__(message, status_code)


class InvalidToken(AdminError):
    def __init__(
        self,
        token_type: TokenType,
        message: str = "Invalid token",
        status_code: int = 401,
    ) -> None:
        super().__init__(message, status_code)
        if token_type == TokenType.ACCESS_TOKEN:
            self.message = "Invalid access token"
            self.status_code = 401
        elif token_type == TokenType.REFRESH_TOKEN:
            self.message = "Invalid refresh token"
            self.status_code = 409


class InvalidRefreshToken(AdminError):
    def __init__(self, message: str = "Invalid token", status_code: int = 409) -> None:
        super().__init__(message, status_code)
