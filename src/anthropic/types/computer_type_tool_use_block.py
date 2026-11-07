from typing_extensions import Literal

from .._models import BaseModel
from .tool_use_caller import ToolUseCaller
from .computer_type_input import ComputerTypeInput

__all__ = ["ComputerTypeToolUseBlock"]


class ComputerTypeToolUseBlock(BaseModel):
    id: str

    caller: ToolUseCaller
    """
    Which party invoked the tool call: the model directly, or a server tool on its
    behalf.
    """

    input: ComputerTypeInput
    """Type a string of text on the keyboard."""

    name: Literal["type"]

    toolset_name: Literal["computer"]

    type: Literal["tool_use"]
