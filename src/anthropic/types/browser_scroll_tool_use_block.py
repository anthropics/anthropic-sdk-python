from typing_extensions import Literal

from .._models import BaseModel
from .tool_use_caller import ToolUseCaller
from .browser_scroll_input import BrowserScrollInput

__all__ = ["BrowserScrollToolUseBlock"]


class BrowserScrollToolUseBlock(BaseModel):
    id: str

    caller: ToolUseCaller
    """
    Which party invoked the tool call: the model directly, or a server tool on its
    behalf.
    """

    input: BrowserScrollInput
    """Scroll at a viewport position. `target` must be a coordinate target."""

    name: Literal["scroll"]

    toolset_name: Literal["browser"]

    type: Literal["tool_use"]
