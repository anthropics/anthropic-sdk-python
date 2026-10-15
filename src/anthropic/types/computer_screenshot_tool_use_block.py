from typing_extensions import Literal

from .._models import BaseModel
from .tool_use_caller import ToolUseCaller
from .computer_screenshot_input import ComputerScreenshotInput

__all__ = ["ComputerScreenshotToolUseBlock"]


class ComputerScreenshotToolUseBlock(BaseModel):
    id: str

    caller: ToolUseCaller
    """
    Which party invoked the tool call: the model directly, or a server tool on its
    behalf.
    """

    input: ComputerScreenshotInput
    """Take a screenshot of the screen."""

    name: Literal["screenshot"]

    toolset_name: Literal["computer"]

    type: Literal["tool_use"]
