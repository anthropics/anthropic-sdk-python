from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaTextDelta"]


class BetaTextDelta(BaseModel):
    text: str

    type: Literal["text_delta"]
