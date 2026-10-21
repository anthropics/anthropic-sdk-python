from typing_extensions import Literal

from .._models import BaseModel
from .tool_use_caller import ToolUseCaller
from .computer_cursor_position_input import ComputerCursorPositionInput

__all__ = ["ComputerCursorPositionToolUseBlock"]


class ComputerCursorPositionToolUseBlock(BaseModel):
    id: str

    caller: ToolUseCaller
    """
    Which party invoked the tool call: the model directly, or a server tool on its
    behalf.
    """

    input: ComputerCursorPositionInput
    """Get the current (x, y) pixel coordinate of the cursor."""

    name: Literal["cursor_position"]

    toolset_name: Literal["computer"]

    type: Literal["tool_use"]
