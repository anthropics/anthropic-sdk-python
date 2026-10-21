from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["OverloadedError"]


class OverloadedError(BaseModel):
    message: str

    type: Literal["overloaded_error"]
