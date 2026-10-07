from typing_extensions import Literal

from .._models import BaseModel
from .tool_use_caller import ToolUseCaller
from .browser_screenshot_input import BrowserScreenshotInput

__all__ = ["BrowserScreenshotToolUseBlock"]


class BrowserScreenshotToolUseBlock(BaseModel):
    id: str

    caller: ToolUseCaller
    """
    Which party invoked the tool call: the model directly, or a server tool on its
    behalf.
    """

    input: BrowserScreenshotInput
    """Capture the current browser viewport."""

    name: Literal["screenshot"]

    toolset_name: Literal["browser"]

    type: Literal["tool_use"]
