from typing_extensions import Literal

from .._models import BaseModel
from .tool_use_caller import ToolUseCaller
from .browser_read_console_input import BrowserReadConsoleInput

__all__ = ["BrowserReadConsoleToolUseBlock"]


class BrowserReadConsoleToolUseBlock(BaseModel):
    id: str

    caller: ToolUseCaller
    """
    Which party invoked the tool call: the model directly, or a server tool on its
    behalf.
    """

    input: BrowserReadConsoleInput
    """
    Return console output (log entries, errors, warnings) accumulated since the
    driver attached to the tab and since the last read, one line per entry. An empty
    result does not mean no traffic for a tab that predates attach.
    """

    name: Literal["read_console"]

    toolset_name: Literal["browser"]

    type: Literal["tool_use"]
