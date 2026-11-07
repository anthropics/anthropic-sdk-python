from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["BetaManagedAgentsStaticBearerCreateParams"]


class BetaManagedAgentsStaticBearerCreateParams(TypedDict, total=False):
    """Parameters for creating a static bearer token credential."""

    token: Required[str]
    """
    The static bearer token to send to the MCP server, such as an API key or
    personal access token.
    """

    mcp_server_url: Required[str]
    """URL of the MCP server this credential authenticates against."""

    type: Required[Literal["static_bearer"]]
