from typing import Optional
from typing_extensions import Literal

from ..._models import BaseModel
from .beta_tool_use_caller import BetaToolUseCaller
from .beta_browser_get_page_text_input import BetaBrowserGetPageTextInput

__all__ = ["BetaBrowserGetPageTextToolUseBlock"]


class BetaBrowserGetPageTextToolUseBlock(BaseModel):
    id: str

    input: BetaBrowserGetPageTextInput
    """
    Return the page's visible text content as plain text, prioritizing article
    content. Suited to articles, documentation, and other text-heavy pages.
    """

    name: Literal["get_page_text"]

    toolset_name: Literal["browser"]

    type: Literal["tool_use"]

    caller: Optional[BetaToolUseCaller] = None
    """
    Which party invoked the tool call: the model directly, or a server tool on its
    behalf.
    """
