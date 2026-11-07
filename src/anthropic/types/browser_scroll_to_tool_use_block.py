from typing_extensions import Literal

from .._models import BaseModel
from .tool_use_caller import ToolUseCaller
from .browser_scroll_to_input import BrowserScrollToInput

__all__ = ["BrowserScrollToToolUseBlock"]


class BrowserScrollToToolUseBlock(BaseModel):
    id: str

    caller: ToolUseCaller
    """
    Which party invoked the tool call: the model directly, or a server tool on its
    behalf.
    """

    input: BrowserScrollToInput
    """Scroll an element into view."""

    name: Literal["scroll_to"]

    toolset_name: Literal["browser"]

    type: Literal["tool_use"]
