from typing import Optional
from typing_extensions import Literal

from ..._models import BaseModel
from .beta_tool_use_caller import BetaToolUseCaller
from .beta_browser_form_input_input import BetaBrowserFormInputInput

__all__ = ["BetaBrowserFormInputToolUseBlock"]


class BetaBrowserFormInputToolUseBlock(BaseModel):
    id: str

    input: BetaBrowserFormInputInput
    """Set the value of a form element (input, textarea, select, checkbox).

    Use a boolean for checkboxes, an option value or text for selects.
    """

    name: Literal["form_input"]

    toolset_name: Literal["browser"]

    type: Literal["tool_use"]

    caller: Optional[BetaToolUseCaller] = None
    """
    Which party invoked the tool call: the model directly, or a server tool on its
    behalf.
    """
