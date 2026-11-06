from __future__ import annotations

import pathlib
from typing import TYPE_CHECKING, Any, cast
from typing_extensions import Literal

import httpx2

from ._utils import extract_property
from ._models import construct_type_or_none

if TYPE_CHECKING:
    from .types.shared.error_type import ErrorType
    from .types.shared.error_details import ErrorDetails

__all__ = [
    "BadRequestError",
    "AuthenticationError",
    "PermissionDeniedError",
    "NotFoundError",
    "RequestTimeoutError",
    "ConflictError",
    "PreconditionFailedError",
    "ContentTooLargeError",
    "UnprocessableEntityError",
    "RateLimitError",
    "RequestHeaderFieldsTooLargeError",
    "ClientClosedRequestError",
    "InternalServerError",
    "HTTPNotImplementedError",
    "ServiceUnavailableError",
    "GatewayTimeoutError",
    "OverloadedError",
    "RetryableError",
    "RequestTooLargeError",
    "DeadlineExceededError",
    "CredentialsError",
    "IdentityTokenFileError",
]


class AnthropicError(Exception):
    pass


class APIError(AnthropicError):
    message: str
    request: httpx2.Request

    body: object | None
    """The API response body.

    If the API responded with a valid JSON structure then this property will be the
    decoded result.

    If it isn't a valid JSON structure then this will be the raw response.

    If there was no response associated with this error then it will be `None`.
    """

    def __init__(self, message: str, request: httpx2.Request, *, body: object | None) -> None:  # noqa: ARG002
        super().__init__(message)
        self.request = request
        self.message = message
        self.body = body


class APIResponseValidationError(APIError):
    response: httpx2.Response
    status_code: int

    def __init__(self, response: httpx2.Response, body: object | None, *, message: str | None = None) -> None:
        super().__init__(message or "Data returned by API invalid for expected schema.", response.request, body=body)
        self.response = response
        self.status_code = response.status_code


class APIWebhookValidationError(APIError):
    pass


class APIStatusError(APIError):
    """Raised when an API response has a status code of 4xx or 5xx."""

    response: httpx2.Response

    status_code: int

    request_id: str | None

    workspace_id: str | None

    api_message: str | None
    """A human-readable explanation of the error.

    Its wording can change, so don't match on it.

    `error.message` from the response body, if present.
    """

    type: ErrorType | None
    """The broad category of the error.

    `error.type` from the response body, if present.
    """

    error_code: str | None
    """A stable code that names the cause.

    `error.details.error_code` from the response body, if present and a string.
    """

    details: ErrorDetails | None
    """Machine-readable detail about the cause of the error.

    `error_code` names the cause; branch on it rather than on `message`. Absent when
    the error has no code. Treat an unrecognized `error_code` as the bare `type`.

    `error.details` from the response body, if present.
    """

    def __init__(self, message: str, *, response: httpx2.Response, body: object | None) -> None:
        # imported here so that modules in `types` can import this one
        from .types.shared.error_details import ErrorDetails

        super().__init__(message, response.request, body=body)
        self.response = response
        self.status_code = response.status_code
        self.request_id = response.headers.get("request-id")
        self.workspace_id = response.headers.get("anthropic-workspace-id")
        self.api_message = extract_property(body, "error", "message")
        self.type = extract_property(body, "error", "type")
        self.error_code = extract_error_code(body)
        self.details = construct_type_or_none(
            value=extract_property(body, "error", "details"), type_=cast(Any, ErrorDetails)
        )


class APIConnectionError(APIError):
    def __init__(self, *, message: str = "Connection error.", request: httpx2.Request) -> None:
        super().__init__(message, request, body=None)


class APITimeoutError(APIConnectionError):
    def __init__(self, request: httpx2.Request) -> None:
        super().__init__(
            message="Request timed out or interrupted. This could be due to a network timeout, dropped connection, or request cancellation. See https://docs.anthropic.com/en/api/errors#long-requests for more details.",
            request=request,
        )


class RetryableError(AnthropicError):
    """An error that opts into the SDK's retry policy: raise it (e.g. from
    middleware) to have the request attempt retried.

    The request is only retried while `max_retries` has not been exhausted;
    once exhausted the error propagates to the caller as-is.
    """


class CredentialsError(AnthropicError):
    """Raised when credentials cannot be loaded from local files, config, or the environment."""


class IdentityTokenFileError(CredentialsError):
    """Raised when the identity token file does not exist, is empty, or cannot be read.

    `path` is the file the provider tried to read (when known), so callers
    waiting for a projected token to appear can retry without parsing the message.
    """

    path: pathlib.Path | None

    def __init__(self, message: str, *, path: pathlib.Path | None = None) -> None:
        super().__init__(message)
        self.path = path


class BadRequestError(APIStatusError):
    status_code: Literal[400] = 400  # pyright: ignore[reportIncompatibleVariableOverride]


class AuthenticationError(APIStatusError):
    status_code: Literal[401] = 401  # pyright: ignore[reportIncompatibleVariableOverride]


class PermissionDeniedError(APIStatusError):
    status_code: Literal[403] = 403  # pyright: ignore[reportIncompatibleVariableOverride]


class NotFoundError(APIStatusError):
    status_code: Literal[404] = 404  # pyright: ignore[reportIncompatibleVariableOverride]


class RequestTimeoutError(APIStatusError):
    status_code: Literal[408] = 408  # pyright: ignore[reportIncompatibleVariableOverride]


class ConflictError(APIStatusError):
    status_code: Literal[409] = 409  # pyright: ignore[reportIncompatibleVariableOverride]


class PreconditionFailedError(APIStatusError):
    status_code: Literal[412] = 412  # pyright: ignore[reportIncompatibleVariableOverride]


class ContentTooLargeError(APIStatusError):
    status_code: Literal[413] = 413  # pyright: ignore[reportIncompatibleVariableOverride]


RequestTooLargeError = ContentTooLargeError
"""Deprecated: use `ContentTooLargeError`."""


class UnprocessableEntityError(APIStatusError):
    status_code: Literal[422] = 422  # pyright: ignore[reportIncompatibleVariableOverride]


class RateLimitError(APIStatusError):
    status_code: Literal[429] = 429  # pyright: ignore[reportIncompatibleVariableOverride]


class RequestHeaderFieldsTooLargeError(APIStatusError):
    status_code: Literal[431] = 431  # pyright: ignore[reportIncompatibleVariableOverride]


class ClientClosedRequestError(APIStatusError):
    status_code: Literal[499] = 499  # pyright: ignore[reportIncompatibleVariableOverride]


class InternalServerError(APIStatusError):
    pass


class HTTPNotImplementedError(InternalServerError):
    status_code: Literal[501] = 501  # pyright: ignore[reportIncompatibleVariableOverride]


class ServiceUnavailableError(InternalServerError):
    status_code: Literal[503] = 503  # pyright: ignore[reportIncompatibleVariableOverride]


class GatewayTimeoutError(InternalServerError):
    status_code: Literal[504] = 504  # pyright: ignore[reportIncompatibleVariableOverride]


DeadlineExceededError = GatewayTimeoutError
"""Deprecated: use `GatewayTimeoutError`."""


class OverloadedError(InternalServerError):
    status_code: Literal[529] = 529  # pyright: ignore[reportIncompatibleVariableOverride]


def extract_error_code(body: object) -> str | None:
    error_code = extract_property(body, "error", "details", "error_code")
    return error_code if isinstance(error_code, str) else None
