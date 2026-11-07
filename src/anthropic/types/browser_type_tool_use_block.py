from typing_extensions import Literal

from .._models import BaseModel
from .tool_use_caller import ToolUseCaller
from .browser_type_input import BrowserTypeInput

__all__ = ["BrowserTypeToolUseBlock"]


class BrowserTypeToolUseBlock(BaseModel):
    id: str

    caller: ToolUseCaller
    """
    Which party invoked the tool call: the model directly, or a server tool on its
    behalf.
    """

    input: BrowserTypeInput
    """Type a literal string at the current focus."""

    name: Literal["type"]

    toolset_name: Literal["browser"]

    type: Literal["tool_use"]
