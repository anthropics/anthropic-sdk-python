from typing import Optional
from typing_extensions import Literal

from ..._models import BaseModel
from .beta_tool_use_caller import BetaToolUseCaller
from .beta_computer_screenshot_input import BetaComputerScreenshotInput

__all__ = ["BetaComputerScreenshotToolUseBlock"]


class BetaComputerScreenshotToolUseBlock(BaseModel):
    id: str

    input: BetaComputerScreenshotInput
    """Take a screenshot of the screen."""

    name: Literal["screenshot"]

    toolset_name: Literal["computer"]

    type: Literal["tool_use"]

    caller: Optional[BetaToolUseCaller] = None
    """
    Which party invoked the tool call: the model directly, or a server tool on its
    behalf.
    """
