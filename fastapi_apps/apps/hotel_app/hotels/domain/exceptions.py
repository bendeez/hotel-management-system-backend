from apps.hotel_app.exceptions import HotelError


class HotelsOverflow(HotelError):
    def __init__(
        self,
        message: str = "Too many hotels have been requested",
        status_code: int = 400,
    ) -> None:
        super().__init__(message, status_code)


class InvalidComparision(HotelError):
    def __init__(
        self,
        message: str = "A 'greater than' value cannot be more than the 'less than' value",
        status_code: int = 400,
    ) -> None:
        super().__init__(message, status_code)
