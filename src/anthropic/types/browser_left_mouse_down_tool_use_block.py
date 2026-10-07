from typing_extensions import Literal

from .._models import BaseModel
from .tool_use_caller import ToolUseCaller
from .browser_left_mouse_down_input import BrowserLeftMouseDownInput

__all__ = ["BrowserLeftMouseDownToolUseBlock"]


class BrowserLeftMouseDownToolUseBlock(BaseModel):
    id: str

    caller: ToolUseCaller
    """
    Which party invoked the tool call: the model directly, or a server tool on its
    behalf.
    """

    input: BrowserLeftMouseDownInput
    """Press and hold the left mouse button at a viewport coordinate.

    Pair with left_mouse_up to perform a custom drag.
    """

    name: Literal["left_mouse_down"]

    toolset_name: Literal["browser"]

    type: Literal["tool_use"]
