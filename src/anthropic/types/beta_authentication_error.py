from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["BetaAuthenticationError"]


class BetaAuthenticationError(BaseModel):
    message: str

    type: Literal["authentication_error"]
