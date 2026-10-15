from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["BetaPermissionError"]


class BetaPermissionError(BaseModel):
    message: str

    type: Literal["permission_error"]
