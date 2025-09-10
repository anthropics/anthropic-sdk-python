# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union, Optional
from typing_extensions import Literal, Required, TypeAlias, TypedDict

from .beta_web_fetch_block_param import BetaWebFetchBlockParam
from .beta_cache_control_ephemeral_param import BetaCacheControlEphemeralParam
from .beta_web_fetch_tool_result_error_block_param import BetaWebFetchToolResultErrorBlockParam

__all__ = ["BetaWebFetchToolResultBlockParam", "Content"]

Content: TypeAlias = Union[BetaWebFetchToolResultErrorBlockParam, BetaWebFetchBlockParam]


class BetaWebFetchToolResultBlockParam(TypedDict, total=False):
    content: Required[Content]

    tool_use_id: Required[str]

    type: Required[Literal["web_fetch_tool_result"]]

    cache_control: Optional[BetaCacheControlEphemeralParam]
    """Create a cache control breakpoint at this content block."""
