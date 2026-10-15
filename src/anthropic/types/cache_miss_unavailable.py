from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["CacheMissUnavailable"]


class CacheMissUnavailable(BaseModel):
    type: Literal["unavailable"]
