from typing_extensions import Literal

from .._exceptions import BadRequestError
from .tool_reference_unresolved_error_details import ToolReferenceUnresolvedErrorDetails

__all__ = ["ToolReferenceUnresolvedError"]


class ToolReferenceUnresolvedError(BadRequestError):
    """
    A tool change or MCP tool listing references a tool or MCP server that is not defined at that position in the conversation.
    """

    error_code: Literal["tool_reference_unresolved"]  # pyright: ignore[reportIncompatibleVariableOverride]
    details: ToolReferenceUnresolvedErrorDetails  # pyright: ignore[reportIncompatibleVariableOverride]
