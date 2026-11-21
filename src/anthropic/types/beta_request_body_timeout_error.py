from typing_extensions import Literal

from .._exceptions import BadRequestError
from .beta_request_body_timeout_error_details import BetaRequestBodyTimeoutErrorDetails

__all__ = ["BetaRequestBodyTimeoutError"]


class BetaRequestBodyTimeoutError(BadRequestError):
    """The request body did not finish arriving in time, so nothing was done.

    Send a smaller body, or send it over a faster connection.
    """

    error_code: Literal["request_body_timeout"]  # pyright: ignore[reportIncompatibleVariableOverride]
    details: BetaRequestBodyTimeoutErrorDetails  # pyright: ignore[reportIncompatibleVariableOverride]
