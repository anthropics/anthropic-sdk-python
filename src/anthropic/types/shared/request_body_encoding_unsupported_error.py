from typing_extensions import Literal

from ..._exceptions import BadRequestError
from .request_body_encoding_unsupported_error_details import RequestBodyEncodingUnsupportedErrorDetails

__all__ = ["RequestBodyEncodingUnsupportedError"]


class RequestBodyEncodingUnsupportedError(BadRequestError):
    """The request's `Content-Encoding` is not supported."""

    error_code: Literal["request_body_encoding_unsupported"]  # pyright: ignore[reportIncompatibleVariableOverride]
    details: RequestBodyEncodingUnsupportedErrorDetails  # pyright: ignore[reportIncompatibleVariableOverride]
