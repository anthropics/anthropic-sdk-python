from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["BetaUnsupportedCharsetErrorDetails"]


class BetaUnsupportedCharsetErrorDetails(BaseModel):
    """
    The request's `Content-Type` header names a charset other than UTF-8, ISO-8859-1 or US-ASCII. Send the request with no charset, or with one of these.
    """

    error_code: Literal["unsupported_charset"]
