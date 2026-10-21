from typing import Dict, Optional

from ..._models import BaseModel

__all__ = ["BetaMCPTool"]


class BetaMCPTool(BaseModel):
    """
    A tool as an MCP server lists it: its name on that server, its
    description, and its input schema.
    """

    input_schema: Dict[str, object]

    name: str

    description: Optional[str] = None
