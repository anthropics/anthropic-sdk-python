from typing_extensions import Literal

from .._models import BaseModel
from .tool_use_caller import ToolUseCaller
from .browser_right_click_input import BrowserRightClickInput

__all__ = ["BrowserRightClickToolUseBlock"]


class BrowserRightClickToolUseBlock(BaseModel):
    id: str

    caller: ToolUseCaller
    """
    Which party invoked the tool call: the model directly, or a server tool on its
    behalf.
    """

    input: BrowserRightClickInput
    """Right-click at a viewport coordinate or on an element by reference."""

    name: Literal["right_click"]

    toolset_name: Literal["browser"]

    type: Literal["tool_use"]
