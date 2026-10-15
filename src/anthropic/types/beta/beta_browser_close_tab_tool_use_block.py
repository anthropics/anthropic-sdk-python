from typing import Optional
from typing_extensions import Literal

from ..._models import BaseModel
from .beta_tool_use_caller import BetaToolUseCaller
from .beta_browser_close_tab_input import BetaBrowserCloseTabInput

__all__ = ["BetaBrowserCloseTabToolUseBlock"]


class BetaBrowserCloseTabToolUseBlock(BaseModel):
    id: str

    input: BetaBrowserCloseTabInput
    """Close the tab with the given tab_id."""

    name: Literal["close_tab"]

    toolset_name: Literal["browser"]

    type: Literal["tool_use"]

    caller: Optional[BetaToolUseCaller] = None
    """
    Which party invoked the tool call: the model directly, or a server tool on its
    behalf.
    """
