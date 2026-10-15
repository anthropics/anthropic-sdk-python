from typing_extensions import Literal

from .._models import BaseModel
from .tool_use_caller import ToolUseCaller
from .computer_wait_input import ComputerWaitInput

__all__ = ["ComputerWaitToolUseBlock"]


class ComputerWaitToolUseBlock(BaseModel):
    id: str

    caller: ToolUseCaller
    """
    Which party invoked the tool call: the model directly, or a server tool on its
    behalf.
    """

    input: ComputerWaitInput
    """Wait for a specified duration."""

    name: Literal["wait"]

    toolset_name: Literal["computer"]

    type: Literal["tool_use"]
