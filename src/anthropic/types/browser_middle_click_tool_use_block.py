from typing_extensions import Literal

from .._models import BaseModel
from .tool_use_caller import ToolUseCaller
from .browser_middle_click_input import BrowserMiddleClickInput

__all__ = ["BrowserMiddleClickToolUseBlock"]


class BrowserMiddleClickToolUseBlock(BaseModel):
    id: str

    caller: ToolUseCaller
    """
    Which party invoked the tool call: the model directly, or a server tool on its
    behalf.
    """

    input: BrowserMiddleClickInput
    """Middle-click at a viewport coordinate or on an element by reference."""

    name: Literal["middle_click"]

    toolset_name: Literal["browser"]

    type: Literal["tool_use"]
