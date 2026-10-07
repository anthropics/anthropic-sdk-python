from typing import Optional
from typing_extensions import Literal

from ..._models import BaseModel
from .beta_tool_use_caller import BetaToolUseCaller
from .beta_computer_type_input import BetaComputerTypeInput

__all__ = ["BetaComputerTypeToolUseBlock"]


class BetaComputerTypeToolUseBlock(BaseModel):
    id: str

    input: BetaComputerTypeInput
    """Type a string of text on the keyboard."""

    name: Literal["type"]

    toolset_name: Literal["computer"]

    type: Literal["tool_use"]

    caller: Optional[BetaToolUseCaller] = None
    """
    Which party invoked the tool call: the model directly, or a server tool on its
    behalf.
    """
