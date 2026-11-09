from typing import Optional
from typing_extensions import Literal

from ..._models import BaseModel
from .beta_tool_use_caller import BetaToolUseCaller
from .beta_browser_read_network_input import BetaBrowserReadNetworkInput

__all__ = ["BetaBrowserReadNetworkToolUseBlock"]


class BetaBrowserReadNetworkToolUseBlock(BaseModel):
    id: str

    input: BetaBrowserReadNetworkInput
    """
    Return the network requests (method, URL, status, MIME type, timing) recorded
    since the driver attached to the tab and since the last read, one line per
    entry. An empty result does not mean no traffic for a tab that predates attach.
    """

    name: Literal["read_network"]

    toolset_name: Literal["browser"]

    type: Literal["tool_use"]

    caller: Optional[BetaToolUseCaller] = None
    """
    Which party invoked the tool call: the model directly, or a server tool on its
    behalf.
    """
