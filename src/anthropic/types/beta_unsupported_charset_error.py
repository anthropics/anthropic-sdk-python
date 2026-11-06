from typing_extensions import Literal

from .._exceptions import BadRequestError
from .beta_unsupported_charset_error_details import BetaUnsupportedCharsetErrorDetails

__all__ = ["BetaUnsupportedCharsetError"]


class BetaUnsupportedCharsetError(BadRequestError):
    """
    The request's `Content-Type` header names a charset other than UTF-8, ISO-8859-1 or US-ASCII. Send the request with no charset, or with one of these.
    """

    error_code: Literal["unsupported_charset"]  # pyright: ignore[reportIncompatibleVariableOverride]
    details: BetaUnsupportedCharsetErrorDetails  # pyright: ignore[reportIncompatibleVariableOverride]
