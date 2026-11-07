from typing import Optional

from ..._models import BaseModel

__all__ = ["BetaMCPToolConfig"]


class BetaMCPToolConfig(BaseModel):
    """Configuration for a specific tool in an MCP toolset."""

    defer_loading: Optional[bool] = None

    enabled: Optional[bool] = None
