from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["BetaNotFoundError"]


class BetaNotFoundError(BaseModel):
    message: str

    type: Literal["not_found_error"]
