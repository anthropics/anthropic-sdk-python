from typing_extensions import Literal

from .._models import BaseModel
from .tool_use_caller import ToolUseCaller
from .browser_double_click_input import BrowserDoubleClickInput

__all__ = ["BrowserDoubleClickToolUseBlock"]


class BrowserDoubleClickToolUseBlock(BaseModel):
    id: str

    caller: ToolUseCaller
    """
    Which party invoked the tool call: the model directly, or a server tool on its
    behalf.
    """

    input: BrowserDoubleClickInput
    """Double left-click at a viewport coordinate or on an element by reference."""

    name: Literal["double_click"]

    toolset_name: Literal["browser"]

    type: Literal["tool_use"]
