from typing import Optional
from typing_extensions import Literal

from ..._models import BaseModel
from .beta_tool_use_caller import BetaToolUseCaller
from .beta_computer_wait_input import BetaComputerWaitInput

__all__ = ["BetaComputerWaitToolUseBlock"]


class BetaComputerWaitToolUseBlock(BaseModel):
    id: str

    input: BetaComputerWaitInput
    """Wait for a specified duration."""

    name: Literal["wait"]

    toolset_name: Literal["computer"]

    type: Literal["tool_use"]

    caller: Optional[BetaToolUseCaller] = None
    """
    Which party invoked the tool call: the model directly, or a server tool on its
    behalf.
    """
