from typing_extensions import Literal

from .._models import BaseModel
from .tool_use_caller import ToolUseCaller
from .computer_key_input import ComputerKeyInput

__all__ = ["ComputerKeyToolUseBlock"]


class ComputerKeyToolUseBlock(BaseModel):
    id: str

    caller: ToolUseCaller
    """
    Which party invoked the tool call: the model directly, or a server tool on its
    behalf.
    """

    input: ComputerKeyInput
    """Press a key or key-combination on the keyboard.

    Use "+" to combine modifiers with a key (e.g. "ctrl+s", "alt+Tab",
    "ctrl+shift+Escape"). Key names are case-insensitive; common names like
    "Return", "Tab", "Escape", "Up", "Down", "Left", "Right", "Home", "End",
    "Page_Up", "Page_Down", "Delete", "BackSpace" are supported.
    """

    name: Literal["key"]

    toolset_name: Literal["computer"]

    type: Literal["tool_use"]
