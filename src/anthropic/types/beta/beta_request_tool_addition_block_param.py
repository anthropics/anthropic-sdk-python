# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union, Optional
from typing_extensions import Literal, Required, TypeAlias, TypedDict

from .beta_cache_control_ephemeral_param import BetaCacheControlEphemeralParam
from .beta_tool_change_tool_reference_param import BetaToolChangeToolReferenceParam
from .beta_tool_change_mcp_tool_reference_param import BetaToolChangeMCPToolReferenceParam
from .beta_tool_change_mcp_toolset_reference_param import BetaToolChangeMCPToolsetReferenceParam

__all__ = ["BetaRequestToolAdditionBlockParam", "Tool"]

Tool: TypeAlias = Union[
    BetaToolChangeToolReferenceParam, BetaToolChangeMCPToolReferenceParam, BetaToolChangeMCPToolsetReferenceParam
]


class BetaRequestToolAdditionBlockParam(TypedDict, total=False):
    """Mid-conversation directive to surface a declared tool.

    ``tool`` references a tool (or MCP toolset) by name from the request's
    ``tools``; it is offered to the model from this point in the
    conversation onward.
    """

    tool: Required[Tool]
    """Reference to a single tool the caller declared directly in `tools[]`.

    Does not accept the composed `{server}_{name}` form the server assigns to
    MCP-resolved tools — use `mcp_tool_reference` or `mcp_toolset_reference` for
    those.
    """

    type: Required[Literal["tool_addition"]]

    cache_control: Optional[BetaCacheControlEphemeralParam]
    """Create a cache control breakpoint at this content block."""
