from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["BetaGatewayTimeoutError"]


class BetaGatewayTimeoutError(BaseModel):
    message: str

    type: Literal["timeout_error"]
