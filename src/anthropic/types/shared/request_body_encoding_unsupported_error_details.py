from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["RequestBodyEncodingUnsupportedErrorDetails"]


class RequestBodyEncodingUnsupportedErrorDetails(BaseModel):
    """The request's `Content-Encoding` is not supported."""

    error_code: Literal["request_body_encoding_unsupported"]
