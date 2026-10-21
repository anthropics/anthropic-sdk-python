from typing import Optional
from typing_extensions import Literal

from ..._models import BaseModel
from .beta_tool_use_caller import BetaToolUseCaller
from .beta_computer_key_input import BetaComputerKeyInput

__all__ = ["BetaComputerKeyToolUseBlock"]


class BetaComputerKeyToolUseBlock(BaseModel):
    id: str

    input: BetaComputerKeyInput
    """Press a key or key-combination on the keyboard.

    Use "+" to combine modifiers with a key (e.g. "ctrl+s", "alt+Tab",
    "ctrl+shift+Escape"). Key names are case-insensitive; common names like
    "Return", "Tab", "Escape", "Up", "Down", "Left", "Right", "Home", "End",
    "Page_Up", "Page_Down", "Delete", "BackSpace" are supported.
    """

    name: Literal["key"]

    toolset_name: Literal["computer"]

    type: Literal["tool_use"]

    caller: Optional[BetaToolUseCaller] = None
    """
    Which party invoked the tool call: the model directly, or a server tool on its
    behalf.
    """
