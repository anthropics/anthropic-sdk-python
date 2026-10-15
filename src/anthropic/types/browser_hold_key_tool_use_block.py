from typing_extensions import Literal

from .._models import BaseModel
from .tool_use_caller import ToolUseCaller
from .browser_hold_key_input import BrowserHoldKeyInput

__all__ = ["BrowserHoldKeyToolUseBlock"]


class BrowserHoldKeyToolUseBlock(BaseModel):
    id: str

    caller: ToolUseCaller
    """
    Which party invoked the tool call: the model directly, or a server tool on its
    behalf.
    """

    input: BrowserHoldKeyInput
    """Hold a key or key chord down for a duration, then release it.

    Uses the same key names and "+" chord syntax as the key action.
    """

    name: Literal["hold_key"]

    toolset_name: Literal["browser"]

    type: Literal["tool_use"]
