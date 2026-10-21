from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["BetaToolChangeToolReferenceParam"]


class BetaToolChangeToolReferenceParam(TypedDict, total=False):
    """
    Reference to a single tool, by the name the model uses to call it: a
    tool declared in ``tools`` or defined by an earlier ``tool_addition``
    block. Does not accept the composed ``{server}_{name}`` form the server
    assigns to MCP-resolved tools; use ``mcp_tool_reference`` or
    ``mcp_toolset_reference`` for those.
    """

    name: Required[str]

    type: Required[Literal["tool_reference"]]
