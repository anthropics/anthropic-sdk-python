# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

from .beta_fallback_info_param import BetaFallbackInfoParam

__all__ = ["BetaFallbackBlockParam"]

_BetaFallbackBlockParamReservedKeywords = TypedDict(
    "_BetaFallbackBlockParamReservedKeywords",
    {
        "from": BetaFallbackInfoParam,
    },
    total=False,
)


class BetaFallbackBlockParam(_BetaFallbackBlockParamReservedKeywords, total=False):
    """A `fallback` block echoed back from a prior response.

    Accepted in `messages[].content` and never rendered into the prompt,
    not validated against the request's `fallbacks` chain or top-level
    `model`, and stripped before the sticky-routing cache key is computed.

    Callers should echo the assistant turn verbatim — block included. The
    block's position is load-bearing for thinking verification: the thinking
    runs on either side of a fallback hop carry independently-rooted
    verification hash chains, and this block is the only record of where one
    chain ends and the next begins. When thinking runs flank the boundary,
    omitting the block merges the runs into one contiguous span whose hashes
    cannot verify (the request is rejected), and moving it into the middle of
    a single run splits that run's chain and is likewise rejected; between
    non-thinking blocks the block's placement has no verification effect.
    """

    to: Required[BetaFallbackInfoParam]
    """Identifies one hop of a fallback transition."""

    type: Required[Literal["fallback"]]
