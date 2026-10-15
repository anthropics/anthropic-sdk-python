from typing_extensions import Literal

from .._models import BaseModel
from .tool_use_caller import ToolUseCaller
from .browser_navigate_input import BrowserNavigateInput

__all__ = ["BrowserNavigateToolUseBlock"]


class BrowserNavigateToolUseBlock(BaseModel):
    id: str

    caller: ToolUseCaller
    """
    Which party invoked the tool call: the model directly, or a server tool on its
    behalf.
    """

    input: BrowserNavigateInput
    """Navigate to a URL, or go back/forward/reload in history.

    The protocol may be omitted (defaults to https://).
    """

    name: Literal["navigate"]

    toolset_name: Literal["browser"]

    type: Literal["tool_use"]
