# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["BetaRedactedThinkingBlockParam"]


class BetaRedactedThinkingBlockParam(TypedDict, total=False):
    data: Required[str]
    """
    The `data` value of this redacted thinking block, exactly as returned by the API
    in a previous response. Opaque and encrypted; pass it back unchanged.
    """

    type: Required[Literal["redacted_thinking"]]
