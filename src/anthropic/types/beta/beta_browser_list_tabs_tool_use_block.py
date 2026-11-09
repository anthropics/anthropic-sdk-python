from typing import Optional
from typing_extensions import Literal

from ..._models import BaseModel
from .beta_tool_use_caller import BetaToolUseCaller
from .beta_browser_list_tabs_input import BetaBrowserListTabsInput

__all__ = ["BetaBrowserListTabsToolUseBlock"]


class BetaBrowserListTabsToolUseBlock(BaseModel):
    id: str

    input: BetaBrowserListTabsInput
    """List all open tabs with each tab's tab_id, title, and URL."""

    name: Literal["list_tabs"]

    toolset_name: Literal["browser"]

    type: Literal["tool_use"]

    caller: Optional[BetaToolUseCaller] = None
    """
    Which party invoked the tool call: the model directly, or a server tool on its
    behalf.
    """
