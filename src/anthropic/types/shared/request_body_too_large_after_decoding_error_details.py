from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["RequestBodyTooLargeAfterDecodingErrorDetails"]


class RequestBodyTooLargeAfterDecodingErrorDetails(BaseModel):
    """The compressed request body exceeds the request size limit once decoded."""

    error_code: Literal["request_body_too_large_after_decoding"]
