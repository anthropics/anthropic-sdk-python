from typing_extensions import Literal

from .._models import BaseModel
from .tool_use_caller import ToolUseCaller
from .browser_left_click_input import BrowserLeftClickInput

__all__ = ["BrowserLeftClickToolUseBlock"]


class BrowserLeftClickToolUseBlock(BaseModel):
    id: str

    caller: ToolUseCaller
    """
    Which party invoked the tool call: the model directly, or a server tool on its
    behalf.
    """

    input: BrowserLeftClickInput
    """Left-click at a viewport coordinate or on an element by reference."""

    name: Literal["left_click"]

    toolset_name: Literal["browser"]

    type: Literal["tool_use"]
