from typing_extensions import Literal

from .._models import BaseModel
from .tool_use_caller import ToolUseCaller
from .browser_switch_tab_input import BrowserSwitchTabInput

__all__ = ["BrowserSwitchTabToolUseBlock"]


class BrowserSwitchTabToolUseBlock(BaseModel):
    id: str

    caller: ToolUseCaller
    """
    Which party invoked the tool call: the model directly, or a server tool on its
    behalf.
    """

    input: BrowserSwitchTabInput
    """
    Make the tab with the given tab_id the active tab — the tab that actions without
    a tab_id apply to.
    """

    name: Literal["switch_tab"]

    toolset_name: Literal["browser"]

    type: Literal["tool_use"]
