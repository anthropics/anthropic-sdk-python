# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable, Optional
from typing_extensions import Literal, Required, TypedDict

from .beta_text_block_param import BetaTextBlockParam
from .beta_cache_control_ephemeral_param import BetaCacheControlEphemeralParam

__all__ = ["BetaMidConversationSystemBlockParam"]


class BetaMidConversationSystemBlockParam(TypedDict, total=False):
    """System instructions that appear mid-conversation.

    Use this block to provide or update system-level instructions at a specific
    point in the conversation, rather than only via the top-level `system` parameter.
    """

    content: Required[Iterable[BetaTextBlockParam]]
    """System instruction text blocks."""

    type: Required[Literal["mid_conv_system"]]

    cache_control: Optional[BetaCacheControlEphemeralParam]
    """Create a cache control breakpoint at this content block."""
