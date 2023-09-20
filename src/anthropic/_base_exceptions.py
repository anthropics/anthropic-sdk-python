from typing_extensions import Literal

from httpx import Request, Response


class APIError(Exception):
    """
    Base exception class for API-related errors.

    Attributes:
        message (str): The error message.
        request (Request): The HTTP request associated with the error.
    """

    def __init__(self, message: str, request: Request) -> None:
        """
        Initialize an APIError.

        Args:
            message (str): The error message.
            request (Request): The HTTP request associated with the error.
        """
        super().__init__(message)
        self.request = request
        self.message = message


class APIResponseValidationError(APIError):
    """
    Exception raised when the data returned by the API is invalid for the expected schema.

    Attributes:
        response (Response): The HTTP response associated with the error.
        status_code (int): The HTTP status code of the response.
    """

    def __init__(self, request: Request, response: Response) -> None:
        """
        Initialize an APIResponseValidationError.

        Args:
            request (Request): The HTTP request associated with the error.
            response (Response): The HTTP response associated with the error.
        """
        super().__init__("Data returned by API invalid for expected schema.", request)
        self.response = response
        self.status_code = response.status_code


class APIStatusError(APIError):
    """
    Exception raised when an API response has a status code of 4xx or 5xx.

    Attributes:
        response (Response): The HTTP response associated with the error.
        status_code (int): The HTTP status code of the response.
        body (object): The API response body. If it's valid JSON, it's decoded; otherwise, it's the raw response.
    """

    response: Response
    status_code: int

    body: object
    """The API response body.

    If the API responded with a valid JSON structure then this property will be the decoded result.
    If it isn't a valid JSON structure then this will be the raw response.
    """

    def __init__(self, message: str, *, request: Request, response: Response, body: object) -> None:
        """
        Initialize an APIStatusError.

        Args:
            message (str): The error message.
            request (Request): The HTTP request associated with the error.
            response (Response): The HTTP response associated with the error.
            body (object): The API response body.
        """

        super().__init__(message, request)
        self.response = response
        self.status_code = response.status_code
        self.body = body


class BadRequestError(APIStatusError):
    """
    Exception raised when an API response has a status code of 400 (Bad Request).

    Attributes:
        status_code (Literal[400]): The HTTP status code (400) of the response.
    """
    status_code: Literal[400]

    def __init__(self, message: str, *, request: Request, response: Response, body: object) -> None:
        super().__init__(message, request=request, response=response, body=body)
        self.status_code = 400


class AuthenticationError(APIStatusError):
    status_code: Literal[401]

    def __init__(self, message: str, *, request: Request, response: Response, body: object) -> None:
        super().__init__(message, request=request, response=response, body=body)
        self.status_code = 401


class PermissionDeniedError(APIStatusError):
    status_code: Literal[403]

    def __init__(self, message: str, *, request: Request, response: Response, body: object) -> None:
        super().__init__(message, request=request, response=response, body=body)
        self.status_code = 403


class NotFoundError(APIStatusError):
    status_code: Literal[404]

    def __init__(self, message: str, *, request: Request, response: Response, body: object) -> None:
        super().__init__(message, request=request, response=response, body=body)
        self.status_code = 404


class ConflictError(APIStatusError):
    status_code: Literal[409]

    def __init__(self, message: str, *, request: Request, response: Response, body: object) -> None:
        super().__init__(message, request=request, response=response, body=body)
        self.status_code = 409


class UnprocessableEntityError(APIStatusError):
    status_code: Literal[422]

    def __init__(self, message: str, *, request: Request, response: Response, body: object) -> None:
        super().__init__(message, request=request, response=response, body=body)
        self.status_code = 422


class RateLimitError(APIStatusError):
    status_code: Literal[429]

    def __init__(self, message: str, *, request: Request, response: Response, body: object) -> None:
        super().__init__(message, request=request, response=response, body=body)
        self.status_code = 429


class InternalServerError(APIStatusError):
    status_code: int

    def __init__(self, message: str, *, request: Request, response: Response, body: object) -> None:
        super().__init__(message, request=request, response=response, body=body)
        self.status_code = response.status_code


class APIConnectionError(APIError):
    def __init__(self, request: Request, message: str = "Connection error.") -> None:
        super().__init__(message, request)


class APITimeoutError(APIConnectionError):
    def __init__(self, request: Request) -> None:
        super().__init__(request, "Request timed out.")
