# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Optional
from typing_extensions import Literal, Required, TypedDict

from ..._types import SequenceNotStr
from .beta_user_location_param import BetaUserLocationParam
from .beta_cache_control_ephemeral_param import BetaCacheControlEphemeralParam

__all__ = ["BetaWebSearchTool20260318Param"]


class BetaWebSearchTool20260318Param(TypedDict, total=False):
    name: Required[Literal["web_search"]]
    """Name of the tool.

    This is how the tool will be called by the model and in `tool_use` blocks.
    """

    type: Required[Literal["web_search_20260318"]]

    allowed_callers: List[
        Literal["direct", "code_execution_20250825", "code_execution_20260120", "code_execution_20260521"]
    ]

    allowed_domains: Optional[SequenceNotStr[str]]
    """If provided, only these domains will be included in results.

    Cannot be used alongside `blocked_domains`.
    """

    blocked_domains: Optional[SequenceNotStr[str]]
    """If provided, these domains will never appear in results.

    Cannot be used alongside `allowed_domains`.
    """

    cache_control: Optional[BetaCacheControlEphemeralParam]
    """Create a cache control breakpoint at this content block."""

    defer_loading: bool
    """If true, tool will not be included in initial system prompt.

    Only loaded when returned via tool_reference from tool search.
    """

    max_uses: Optional[int]
    """Maximum number of times the tool can be used in the API request."""

    response_inclusion: Literal["full", "excluded"]
    """
    How this tool's result blocks appear in the API response when the result was
    consumed by a completed code_execution call in the same turn. 'full' returns the
    complete content (default). 'excluded' drops the nested server_tool_use and
    result block pair entirely. Results from direct calls, or from code_execution
    calls that paused before completing, are always returned in full so they can be
    sent back on the next turn.
    """

    strict: bool
    """When true, guarantees schema validation on tool names and inputs"""

    user_location: Optional[BetaUserLocationParam]
    """Parameters for the user's location.

    Used to provide more relevant search results.
    """
