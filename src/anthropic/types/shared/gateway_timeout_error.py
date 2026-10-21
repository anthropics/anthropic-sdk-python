from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["GatewayTimeoutError"]


class GatewayTimeoutError(BaseModel):
    message: str

    type: Literal["timeout_error"]
