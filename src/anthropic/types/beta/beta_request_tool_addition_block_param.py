from __future__ import annotations

from typing import Union, Optional
from typing_extensions import Literal, Required, TypeAlias, TypedDict

from .beta_cache_control_ephemeral_param import BetaCacheControlEphemeralParam
from .beta_tool_change_tool_reference_param import BetaToolChangeToolReferenceParam
from .beta_tool_change_tool_definition_param import BetaToolChangeToolDefinitionParam
from .beta_tool_change_mcp_tool_reference_param import BetaToolChangeMCPToolReferenceParam
from .beta_tool_change_mcp_toolset_reference_param import BetaToolChangeMCPToolsetReferenceParam

__all__ = ["BetaRequestToolAdditionBlockParam", "Tool"]

Tool: TypeAlias = Union[
    BetaToolChangeToolReferenceParam,
    BetaToolChangeMCPToolReferenceParam,
    BetaToolChangeMCPToolsetReferenceParam,
    BetaToolChangeToolDefinitionParam,
]


class BetaRequestToolAdditionBlockParam(TypedDict, total=False):
    """Mid-conversation directive to make a tool available.

    ``tool`` is a reference to a tool (or MCP toolset) declared in the
    request's ``tools``. Under the ``inline-tools-2026-09-15`` beta it may
    instead be a reference to a tool defined earlier in ``messages``, or a
    ``tool_definition`` object that carries an inline tool definition in
    ``definition`` (the same object a ``tools`` entry holds). An ``mcp_toolset``
    definition also requires the ``mcp-client-2026-09-15`` beta. The tool is
    offered to the model from this point in the conversation onward.
    """

    tool: Required[Tool]

    type: Required[Literal["tool_addition"]]

    cache_control: Optional[BetaCacheControlEphemeralParam]
    """Create a cache control breakpoint at this content block."""
