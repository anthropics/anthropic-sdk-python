from typing import Optional
from typing_extensions import Literal

from ..._models import BaseModel
from .beta_tool_use_caller import BetaToolUseCaller
from .beta_browser_screenshot_input import BetaBrowserScreenshotInput

__all__ = ["BetaBrowserScreenshotToolUseBlock"]


class BetaBrowserScreenshotToolUseBlock(BaseModel):
    id: str

    input: BetaBrowserScreenshotInput
    """Capture the current browser viewport."""

    name: Literal["screenshot"]

    toolset_name: Literal["browser"]

    type: Literal["tool_use"]

    caller: Optional[BetaToolUseCaller] = None
    """
    Which party invoked the tool call: the model directly, or a server tool on its
    behalf.
    """
