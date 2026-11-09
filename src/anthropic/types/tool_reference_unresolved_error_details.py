from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["ToolReferenceUnresolvedErrorDetails"]


class ToolReferenceUnresolvedErrorDetails(BaseModel):
    """
    A tool change or MCP tool listing references a tool or MCP server that is not defined at that position in the conversation.
    """

    error_code: Literal["tool_reference_unresolved"]
