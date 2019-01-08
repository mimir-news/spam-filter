# Standard library
import json
from uuid import uuid4
from typing import Dict, Any

# 3rd party modules
from flask import request

# Internal modules
from app.controllers import status


class RequestError(Exception):
    """Exception that can be raised when request failed.

    message: Error message as a string.
    """

    def __init__(self, message: str) -> None:
        self.id = str(uuid4()).lower()
        self.message = message

    def __str__(self) -> str:
        return json.dumps(self.asdict())

    def asdict(self) -> Dict[str, Any]:
        return {
            "errorId": self.id,
            "status": self.status(),
            "message": self.message,
            "path": request.path,
            "requestId": request.id,
        }

    def status(self) -> int:
        return status.HTTP_500_INTERNAL_SERVER_ERROR


class BadRequestError(RequestError):
    """Exception that can be thrown when a bad request has beed recieved.

    message: Error message as a string.
    """

    def status(self) -> int:
        return status.HTTP_400_BAD_REQUEST


class ConflictError(RequestError):
    """Exception that can be thrown when a conflicting has beed recieved.

    message: Error message as a string.
    """

    def status(self) -> int:
        return status.HTTP_409_CONFLICT


class NotFoundError(RequestError):
    """Exception that can be thrown when a conflicting has beed recieved.

    message: Error message as a string.
    """

    def status(self) -> int:
        return status.HTTP_404_NOT_FOUND


class InternalServerError(RequestError):
    """Exception that can be thrown when a conflicting has beed recieved.

    message: Error message as a string.
    """

    def __init__(self, message="Internal error"):
        super().__init__(message)


class NotImplementedError(RequestError):
    """Exception that can be thrown when request was made to
    an endpoint that has not yet been implemented.

    message: Error message as a string.
    """

    def __init__(self) -> None:
        super().__init__("Not implemented")

    def status(self) -> int:
        return status.HTTP_501_NOT_IMPLEMENTED
