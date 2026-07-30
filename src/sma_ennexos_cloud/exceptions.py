class SmaError(Exception):
    """Base exception for SMA ennexOS library."""


class AuthenticationError(SmaError):
    """Raised when authentication fails."""


class APIError(SmaError):
    """Raised when the SMA API returns an error."""

    def __init__(self, message: str, status_code: int | None = None) -> None:
        super().__init__(message)
        self.status_code = status_code
