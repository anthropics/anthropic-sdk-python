from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaRawContentBlockStopEvent"]


class BetaRawContentBlockStopEvent(BaseModel):
    index: int

    type: Literal["content_block_stop"]
