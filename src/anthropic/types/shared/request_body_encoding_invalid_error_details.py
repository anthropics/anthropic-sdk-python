from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["RequestBodyEncodingInvalidErrorDetails"]


class RequestBodyEncodingInvalidErrorDetails(BaseModel):
    """The request body is not valid for its `Content-Encoding`."""

    error_code: Literal["request_body_encoding_invalid"]
