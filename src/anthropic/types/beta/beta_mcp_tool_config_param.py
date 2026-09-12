from __future__ import annotations

from typing_extensions import TypedDict

__all__ = ["BetaMCPToolConfigParam"]


class BetaMCPToolConfigParam(TypedDict, total=False):
    """Configuration for a specific tool in an MCP toolset."""

    defer_loading: bool

    enabled: bool
