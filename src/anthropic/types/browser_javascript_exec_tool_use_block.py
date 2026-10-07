from typing_extensions import Literal

from .._models import BaseModel
from .tool_use_caller import ToolUseCaller
from .browser_javascript_exec_input import BrowserJavascriptExecInput

__all__ = ["BrowserJavascriptExecToolUseBlock"]


class BrowserJavascriptExecToolUseBlock(BaseModel):
    id: str

    caller: ToolUseCaller
    """
    Which party invoked the tool call: the model directly, or a server tool on its
    behalf.
    """

    input: BrowserJavascriptExecInput
    """
    Execute JavaScript in the page context and return the value of the last
    expression. The code runs with access to the DOM, `window`, and page variables.
    Write the expression you want evaluated — do NOT use `return`.
    """

    name: Literal["javascript_exec"]

    toolset_name: Literal["browser"]

    type: Literal["tool_use"]
