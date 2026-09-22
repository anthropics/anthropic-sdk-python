from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaResponseToolChangeMCPToolsetReference"]


class BetaResponseToolChangeMCPToolsetReference(BaseModel):
    """
    Reference to every tool in the named MCP server's toolset, as a
    ``compaction`` block's ``tool_changes`` entry reports it. Send it back
    unchanged with the block.
    """

    server_name: str

    type: Literal["mcp_toolset_reference"]
