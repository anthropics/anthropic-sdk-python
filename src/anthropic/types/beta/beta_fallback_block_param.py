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

    Accepted in `messages[].content` and not rendered into the prompt; not
    validated against the request's `fallbacks` chain or top-level `model`.

    Echo the assistant turn back verbatim, including this block in its
    original position. The block marks the boundary between content produced
    before and after a fallback hop, and the server relies on that boundary
    to validate the turn: when thinking runs flank the boundary, omitting
    the block merges them into one span the server cannot validate (the
    request is rejected), and moving it into the middle of a single run is
    likewise rejected; between non-thinking blocks the block's placement has
    no validation effect.
    """

    to: Required[BetaFallbackInfoParam]
    """Identifies one hop of a fallback transition."""

    type: Required[Literal["fallback"]]

    trigger: object
    """The response block's `trigger`, echoed verbatim.

    Accepted and ignored by the server; any object or `null` is allowed.
    """
