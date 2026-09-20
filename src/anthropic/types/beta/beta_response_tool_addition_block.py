from typing import Union
from typing_extensions import Literal, Annotated, TypeAlias

from ..._models import BaseModel, UnionDiscriminator
from .beta_tool_change_tool_definition import BetaToolChangeToolDefinition
from .beta_response_tool_change_tool_reference import BetaResponseToolChangeToolReference
from .beta_response_tool_change_mcp_tool_reference import BetaResponseToolChangeMCPToolReference
from .beta_response_tool_change_mcp_toolset_reference import BetaResponseToolChangeMCPToolsetReference

__all__ = ["BetaResponseToolAdditionBlock", "Tool"]

Tool: TypeAlias = Annotated[
    Union[
        BetaResponseToolChangeToolReference,
        BetaResponseToolChangeMCPToolReference,
        BetaResponseToolChangeMCPToolsetReference,
        BetaToolChangeToolDefinition,
    ],
    UnionDiscriminator("type"),
]


class BetaResponseToolAdditionBlock(BaseModel):
    """
    An entry of a `compaction` block's `tool_changes`: a tool the
    compacted range made available, as a reference to a `tools` entry or
    MCP toolset, or as the tool definition in effect at the end of the
    range, by value. Send it back unchanged.
    """

    tool: Tool
    """
    The tool made available: a reference to a `tools` entry or MCP toolset, or a
    `tool_definition` carrying the definition by value.
    """

    type: Literal["tool_addition"]
