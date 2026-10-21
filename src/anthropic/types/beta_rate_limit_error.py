from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["BetaRateLimitError"]


class BetaRateLimitError(BaseModel):
    message: str

    type: Literal["rate_limit_error"]
