# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing_extensions import Literal

from pydantic import Field as FieldInfo

from ..._models import BaseModel
from .beta_fallback_info import BetaFallbackInfo

__all__ = ["BetaFallbackBlock"]


class BetaFallbackBlock(BaseModel):
    """Marks the point in `content` where one model's output gives way to the next.

    One block appears per hop where a preceding model actually ran this turn and
    declined. A turn routed directly by the sticky decision has no such boundary
    and carries no block — the signal for whether a fallback model served the
    response is the presence of a `fallback_message` entry in
    `usage.iterations`, not this block.

    The block is treated like a server-tool content block for streaming: it
    arrives via the standard `content_block_start` / `content_block_stop`
    pair and carries no deltas.
    """

    from_: BetaFallbackInfo = FieldInfo(alias="from")
    """The model whose output ends at this point — the model that declined at this hop.

    When the declining hop is the requested model, its `model` echoes the top-level
    `model` string the caller sent (alias or canonical); when the declining hop is a
    fallback model, its `model` is that model's canonical id.
    """

    to: BetaFallbackInfo
    """The fallback model producing the content that follows this block.

    Its `model` is always the canonical id.
    """

    type: Literal["fallback"]
