from typing import Any


class DomainError(Exception):
    def __init__(
            self,
            message: str,
            details: None | dict[str, Any] = None,
    ):
        self.details = details
        self.message = message
        super().__init__(message)


    def __str__(self) -> str:
        return f"{self.__class__.__name__}: {self.message}"