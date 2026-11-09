from typing_extensions import Literal

from ..._exceptions import ContentTooLargeError
from .request_body_too_large_after_decoding_error_details import RequestBodyTooLargeAfterDecodingErrorDetails

__all__ = ["RequestBodyTooLargeAfterDecodingError"]


class RequestBodyTooLargeAfterDecodingError(ContentTooLargeError):
    """The compressed request body exceeds the request size limit once decoded."""

    error_code: Literal["request_body_too_large_after_decoding"]  # pyright: ignore[reportIncompatibleVariableOverride]
    details: RequestBodyTooLargeAfterDecodingErrorDetails  # pyright: ignore[reportIncompatibleVariableOverride]
