from typing_extensions import Literal

from .._models import BaseModel
from .tool_use_caller import ToolUseCaller
from .computer_hold_key_input import ComputerHoldKeyInput

__all__ = ["ComputerHoldKeyToolUseBlock"]


class ComputerHoldKeyToolUseBlock(BaseModel):
    id: str

    caller: ToolUseCaller
    """
    Which party invoked the tool call: the model directly, or a server tool on its
    behalf.
    """

    input: ComputerHoldKeyInput
    """Hold down a key or key-combination for a specified duration.

    Uses the same key syntax as `key`.
    """

    name: Literal["hold_key"]

    toolset_name: Literal["computer"]

    type: Literal["tool_use"]
