from typing_extensions import Literal

from .._models import BaseModel
from .tool_use_caller import ToolUseCaller
from .browser_mouse_move_input import BrowserMouseMoveInput

__all__ = ["BrowserMouseMoveToolUseBlock"]


class BrowserMouseMoveToolUseBlock(BaseModel):
    id: str

    caller: ToolUseCaller
    """
    Which party invoked the tool call: the model directly, or a server tool on its
    behalf.
    """

    input: BrowserMouseMoveInput
    """Move the pointer to a viewport coordinate without clicking."""

    name: Literal["mouse_move"]

    toolset_name: Literal["browser"]

    type: Literal["tool_use"]
