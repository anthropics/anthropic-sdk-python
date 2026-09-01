# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Literal, TypedDict

__all__ = ["BetaSystemMessageOutputConfigParam"]


class BetaSystemMessageOutputConfigParam(TypedDict, total=False):
    """Per-message output configuration on a role:"system" input message.

    Fields here apply per-turn; ``format`` remains top-level only. An
    empty ``{}`` is accepted on a message that carries content; a message
    with neither content nor output_config fields is rejected.
    """

    effort: Optional[Literal["low", "medium", "high", "xhigh", "max"]]
    """All possible effort levels."""
