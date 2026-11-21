from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["BetaGatewayTimeoutErrorObject"]


class BetaGatewayTimeoutErrorObject(BaseModel):
    message: str
    """A human-readable explanation of the error.

    Its wording can change, so don't match on it.
    """

    type: Literal["timeout_error"]
    """The broad category of the error."""
