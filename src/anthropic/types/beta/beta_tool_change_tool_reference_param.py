# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["BetaToolChangeToolReferenceParam"]


class BetaToolChangeToolReferenceParam(TypedDict, total=False):
    """Reference to a single tool the caller declared directly in
    ``tools[]``.

    Does not accept the composed ``{server}_{name}`` form the
    server assigns to MCP-resolved tools — use ``mcp_tool_reference`` or
    ``mcp_toolset_reference`` for those.
    """

    name: Required[str]

    type: Required[Literal["tool_reference"]]
