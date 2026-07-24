# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["BetaToolChangeMCPToolsetReferenceParam"]


class BetaToolChangeMCPToolsetReferenceParam(TypedDict, total=False):
    """Reference to every tool in the named MCP server's toolset."""

    server_name: Required[str]

    type: Required[Literal["mcp_toolset_reference"]]
