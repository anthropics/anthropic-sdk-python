from typing import Optional
from typing_extensions import Literal

from ..._models import BaseModel
from .beta_tool_use_caller import BetaToolUseCaller
from .beta_browser_javascript_exec_input import BetaBrowserJavascriptExecInput

__all__ = ["BetaBrowserJavascriptExecToolUseBlock"]


class BetaBrowserJavascriptExecToolUseBlock(BaseModel):
    id: str

    input: BetaBrowserJavascriptExecInput
    """
    Execute JavaScript in the page context and return the value of the last
    expression. The code runs with access to the DOM, `window`, and page variables.
    Write the expression you want evaluated — do NOT use `return`.
    """

    name: Literal["javascript_exec"]

    toolset_name: Literal["browser"]

    type: Literal["tool_use"]

    caller: Optional[BetaToolUseCaller] = None
    """
    Which party invoked the tool call: the model directly, or a server tool on its
    behalf.
    """
