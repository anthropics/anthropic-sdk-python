from typing_extensions import Literal

from .._models import BaseModel
from .tool_use_caller import ToolUseCaller
from .browser_form_input_input import BrowserFormInputInput

__all__ = ["BrowserFormInputToolUseBlock"]


class BrowserFormInputToolUseBlock(BaseModel):
    id: str

    caller: ToolUseCaller
    """
    Which party invoked the tool call: the model directly, or a server tool on its
    behalf.
    """

    input: BrowserFormInputInput
    """Set the value of a form element (input, textarea, select, checkbox).

    Use a boolean for checkboxes, an option value or text for selects.
    """

    name: Literal["form_input"]

    toolset_name: Literal["browser"]

    type: Literal["tool_use"]
