from typing_extensions import Literal

from .._models import BaseModel
from .tool_use_caller import ToolUseCaller
from .browser_get_page_text_input import BrowserGetPageTextInput

__all__ = ["BrowserGetPageTextToolUseBlock"]


class BrowserGetPageTextToolUseBlock(BaseModel):
    id: str

    caller: ToolUseCaller
    """
    Which party invoked the tool call: the model directly, or a server tool on its
    behalf.
    """

    input: BrowserGetPageTextInput
    """
    Return the page's visible text content as plain text, prioritizing article
    content. Suited to articles, documentation, and other text-heavy pages.
    """

    name: Literal["get_page_text"]

    toolset_name: Literal["browser"]

    type: Literal["tool_use"]
