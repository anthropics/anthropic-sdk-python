from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["ToolNameConflictErrorDetails"]


class ToolNameConflictErrorDetails(BaseModel):
    """
    A tool made available in `messages` takes a name that an available tool of another kind, or of another MCP server, already holds.
    """

    error_code: Literal["tool_name_conflict"]
