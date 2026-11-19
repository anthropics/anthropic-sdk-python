from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["BetaRequestBodyTimeoutErrorDetails"]


class BetaRequestBodyTimeoutErrorDetails(BaseModel):
    """The request body did not finish arriving in time, so nothing was done.

    Send a smaller body, or send it over a faster connection.
    """

    error_code: Literal["request_body_timeout"]
