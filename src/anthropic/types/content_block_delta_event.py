# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing_extensions import Literal

from .._models import BaseModel
from .text_delta import TextDelta

__all__ = ["ContentBlockDeltaEvent"]


class ContentBlockDeltaEvent(BaseModel):
    delta: TextDelta

    index: int

    type: Literal["content_block_delta"]
