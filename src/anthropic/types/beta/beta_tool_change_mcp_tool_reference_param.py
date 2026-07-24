# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["BetaToolChangeMCPToolReferenceParam"]


class BetaToolChangeMCPToolReferenceParam(TypedDict, total=False):
    """
    Reference to a single MCP tool by its server and remote name — the
    same ``server_name``/``name`` pair ``mcp_tool_use`` carries.
    """

    name: Required[str]

    server_name: Required[str]

    type: Required[Literal["mcp_tool_reference"]]
