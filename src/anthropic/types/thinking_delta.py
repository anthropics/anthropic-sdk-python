# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["ThinkingDelta"]


class ThinkingDelta(BaseModel):
    thinking: str
    """The incremental `thinking` text for this content block.

    Concatenate the `thinking` values of successive `thinking_delta` events to
    assemble the block's full `thinking` value.
    """

    type: Literal["thinking_delta"]
