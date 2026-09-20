from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

from .beta_tool_union_param import BetaToolUnionParam

__all__ = ["BetaToolChangeToolDefinitionParam"]


class BetaToolChangeToolDefinitionParam(TypedDict, total=False):
    """
    A tool defined by value: `definition` is a `tools` entry (any kind
    `tools` accepts, an MCP toolset included). An `mcp_toolset` given here
    also requires the `mcp-client-2026-09-15` beta.
    """

    definition: Required[BetaToolUnionParam]

    type: Required[Literal["tool_definition"]]
