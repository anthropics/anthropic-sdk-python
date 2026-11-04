from typing_extensions import Literal

from ..._exceptions import BadRequestError
from .request_body_encoding_invalid_error_details import RequestBodyEncodingInvalidErrorDetails

__all__ = ["RequestBodyEncodingInvalidError"]


class RequestBodyEncodingInvalidError(BadRequestError):
    """The request body is not valid for its `Content-Encoding`."""

    error_code: Literal["request_body_encoding_invalid"]  # pyright: ignore[reportIncompatibleVariableOverride]
    details: RequestBodyEncodingInvalidErrorDetails  # pyright: ignore[reportIncompatibleVariableOverride]
