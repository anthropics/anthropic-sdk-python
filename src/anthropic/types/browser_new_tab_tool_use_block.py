from typing_extensions import Literal

from .._models import BaseModel
from .tool_use_caller import ToolUseCaller
from .browser_new_tab_input import BrowserNewTabInput

__all__ = ["BrowserNewTabToolUseBlock"]


class BrowserNewTabToolUseBlock(BaseModel):
    id: str

    caller: ToolUseCaller
    """
    Which party invoked the tool call: the model directly, or a server tool on its
    behalf.
    """

    input: BrowserNewTabInput
    """Open a new empty tab and return its tab_id."""

    name: Literal["new_tab"]

    toolset_name: Literal["browser"]

    type: Literal["tool_use"]
