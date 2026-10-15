from typing import Optional
from typing_extensions import Literal

from ..._models import BaseModel
from .beta_tool_use_caller import BetaToolUseCaller
from .beta_browser_new_tab_input import BetaBrowserNewTabInput

__all__ = ["BetaBrowserNewTabToolUseBlock"]


class BetaBrowserNewTabToolUseBlock(BaseModel):
    id: str

    input: BetaBrowserNewTabInput
    """Open a new empty tab and return its tab_id."""

    name: Literal["new_tab"]

    toolset_name: Literal["browser"]

    type: Literal["tool_use"]

    caller: Optional[BetaToolUseCaller] = None
    """
    Which party invoked the tool call: the model directly, or a server tool on its
    behalf.
    """
