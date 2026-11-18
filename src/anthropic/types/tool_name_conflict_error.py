from typing_extensions import Literal

from .._exceptions import BadRequestError
from .tool_name_conflict_error_details import ToolNameConflictErrorDetails

__all__ = ["ToolNameConflictError"]


class ToolNameConflictError(BadRequestError):
    """
    A tool made available in `messages` takes a name that an available tool of another kind, or of another MCP server, already holds.
    """

    error_code: Literal["tool_name_conflict"]  # pyright: ignore[reportIncompatibleVariableOverride]
    details: ToolNameConflictErrorDetails  # pyright: ignore[reportIncompatibleVariableOverride]
