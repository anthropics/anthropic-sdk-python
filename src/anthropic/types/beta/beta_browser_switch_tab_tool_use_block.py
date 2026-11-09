from typing import Optional
from typing_extensions import Literal

from ..._models import BaseModel
from .beta_tool_use_caller import BetaToolUseCaller
from .beta_browser_switch_tab_input import BetaBrowserSwitchTabInput

__all__ = ["BetaBrowserSwitchTabToolUseBlock"]


class BetaBrowserSwitchTabToolUseBlock(BaseModel):
    id: str

    input: BetaBrowserSwitchTabInput
    """
    Make the tab with the given tab_id the active tab — the tab that actions without
    a tab_id apply to.
    """

    name: Literal["switch_tab"]

    toolset_name: Literal["browser"]

    type: Literal["tool_use"]

    caller: Optional[BetaToolUseCaller] = None
    """
    Which party invoked the tool call: the model directly, or a server tool on its
    behalf.
    """
