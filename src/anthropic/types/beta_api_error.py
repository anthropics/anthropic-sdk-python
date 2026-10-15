from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["BetaAPIError"]


class BetaAPIError(BaseModel):
    message: str

    type: Literal["api_error"]
