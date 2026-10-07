from typing_extensions import Literal

from .._models import BaseModel
from .tool_use_caller import ToolUseCaller
from .computer_mouse_move_input import ComputerMouseMoveInput

__all__ = ["ComputerMouseMoveToolUseBlock"]


class ComputerMouseMoveToolUseBlock(BaseModel):
    id: str

    caller: ToolUseCaller
    """
    Which party invoked the tool call: the model directly, or a server tool on its
    behalf.
    """

    input: ComputerMouseMoveInput
    """Move the cursor to a specified (x, y) pixel coordinate.

    Use this ONLY to hover without clicking; otherwise use a click action directly.
    """

    name: Literal["mouse_move"]

    toolset_name: Literal["computer"]

    type: Literal["tool_use"]
