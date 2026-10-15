from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["BetaOverloadedError"]


class BetaOverloadedError(BaseModel):
    message: str

    type: Literal["overloaded_error"]
