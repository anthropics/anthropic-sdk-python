from typing_extensions import Literal

from .._models import BaseModel
from .tool_use_caller import ToolUseCaller
from .browser_left_click_drag_input import BrowserLeftClickDragInput

__all__ = ["BrowserLeftClickDragToolUseBlock"]


class BrowserLeftClickDragToolUseBlock(BaseModel):
    id: str

    caller: ToolUseCaller
    """
    Which party invoked the tool call: the model directly, or a server tool on its
    behalf.
    """

    input: BrowserLeftClickDragInput
    """Press at `from`, drag to `target`, release. Both must be coordinate targets."""

    name: Literal["left_click_drag"]

    toolset_name: Literal["browser"]

    type: Literal["tool_use"]
