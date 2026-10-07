from typing_extensions import Literal

from .._models import BaseModel
from .tool_use_caller import ToolUseCaller
from .browser_list_tabs_input import BrowserListTabsInput

__all__ = ["BrowserListTabsToolUseBlock"]


class BrowserListTabsToolUseBlock(BaseModel):
    id: str

    caller: ToolUseCaller
    """
    Which party invoked the tool call: the model directly, or a server tool on its
    behalf.
    """

    input: BrowserListTabsInput
    """List all open tabs with each tab's tab_id, title, and URL."""

    name: Literal["list_tabs"]

    toolset_name: Literal["browser"]

    type: Literal["tool_use"]
