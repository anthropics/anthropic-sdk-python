from typing_extensions import Literal

from .._models import BaseModel
from .tool_use_caller import ToolUseCaller
from .browser_left_mouse_up_input import BrowserLeftMouseUpInput

__all__ = ["BrowserLeftMouseUpToolUseBlock"]


class BrowserLeftMouseUpToolUseBlock(BaseModel):
    id: str

    caller: ToolUseCaller
    """
    Which party invoked the tool call: the model directly, or a server tool on its
    behalf.
    """

    input: BrowserLeftMouseUpInput
    """Release the left mouse button at a viewport coordinate."""

    name: Literal["left_mouse_up"]

    toolset_name: Literal["browser"]

    type: Literal["tool_use"]
