from typing_extensions import Literal

from .._models import BaseModel
from .tool_use_caller import ToolUseCaller
from .browser_close_tab_input import BrowserCloseTabInput

__all__ = ["BrowserCloseTabToolUseBlock"]


class BrowserCloseTabToolUseBlock(BaseModel):
    id: str

    caller: ToolUseCaller
    """
    Which party invoked the tool call: the model directly, or a server tool on its
    behalf.
    """

    input: BrowserCloseTabInput
    """Close the tab with the given tab_id."""

    name: Literal["close_tab"]

    toolset_name: Literal["browser"]

    type: Literal["tool_use"]
