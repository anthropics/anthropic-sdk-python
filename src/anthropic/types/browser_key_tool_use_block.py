from typing_extensions import Literal

from .._models import BaseModel
from .tool_use_caller import ToolUseCaller
from .browser_key_input import BrowserKeyInput

__all__ = ["BrowserKeyToolUseBlock"]


class BrowserKeyToolUseBlock(BaseModel):
    id: str

    caller: ToolUseCaller
    """
    Which party invoked the tool call: the model directly, or a server tool on its
    behalf.
    """

    input: BrowserKeyInput
    """Press a key or key chord.

    Use "+" to combine modifiers with a key (e.g. "ctrl+a", "cmd+shift+p") and space
    to sequence presses (e.g. "Backspace Backspace Delete"). Common names like
    "Return", "Tab", "Escape", "BackSpace" are supported.
    """

    name: Literal["key"]

    toolset_name: Literal["browser"]

    type: Literal["tool_use"]
