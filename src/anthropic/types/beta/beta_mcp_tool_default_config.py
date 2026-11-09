from typing import Optional

from ..._models import BaseModel

__all__ = ["BetaMCPToolDefaultConfig"]


class BetaMCPToolDefaultConfig(BaseModel):
    """Default configuration for tools in an MCP toolset."""

    defer_loading: Optional[bool] = None

    enabled: Optional[bool] = None
