from typing_extensions import Literal

from .._models import BaseModel
from .tool_use_caller import ToolUseCaller
from .browser_wait_input import BrowserWaitInput

__all__ = ["BrowserWaitToolUseBlock"]


class BrowserWaitToolUseBlock(BaseModel):
    id: str

    caller: ToolUseCaller
    """
    Which party invoked the tool call: the model directly, or a server tool on its
    behalf.
    """

    input: BrowserWaitInput
    """Pause for the given duration."""

    name: Literal["wait"]

    toolset_name: Literal["browser"]

    type: Literal["tool_use"]
