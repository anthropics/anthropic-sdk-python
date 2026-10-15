from typing import Optional
from typing_extensions import Literal

from ..._models import BaseModel
from .beta_tool_use_caller import BetaToolUseCaller
from .beta_browser_key_input import BetaBrowserKeyInput

__all__ = ["BetaBrowserKeyToolUseBlock"]


class BetaBrowserKeyToolUseBlock(BaseModel):
    id: str

    input: BetaBrowserKeyInput
    """Press a key or key chord.

    Use "+" to combine modifiers with a key (e.g. "ctrl+a", "cmd+shift+p") and space
    to sequence presses (e.g. "Backspace Backspace Delete"). Common names like
    "Return", "Tab", "Escape", "BackSpace" are supported.
    """

    name: Literal["key"]

    toolset_name: Literal["browser"]

    type: Literal["tool_use"]

    caller: Optional[BetaToolUseCaller] = None
    """
    Which party invoked the tool call: the model directly, or a server tool on its
    behalf.
    """
