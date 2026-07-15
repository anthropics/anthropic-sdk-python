# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable, Optional
from typing_extensions import Literal, Required, TypedDict

from .text_block_param import TextBlockParam
from .cache_control_ephemeral_param import CacheControlEphemeralParam

__all__ = ["MidConversationSystemBlockParam"]


class MidConversationSystemBlockParam(TypedDict, total=False):
    """System instructions that appear mid-conversation.

    Use this block to provide or update system-level instructions at a specific
    point in the conversation, rather than only via the top-level `system` parameter.
    """

    content: Required[Iterable[TextBlockParam]]
    """System instruction text blocks."""

    type: Required[Literal["mid_conv_system"]]

    cache_control: Optional[CacheControlEphemeralParam]
    """Create a cache control breakpoint at this content block."""
