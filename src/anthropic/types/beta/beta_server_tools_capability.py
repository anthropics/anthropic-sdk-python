from ..._models import BaseModel
from .beta_capability_support import BetaCapabilitySupport

__all__ = ["BetaServerToolsCapability"]


class BetaServerToolsCapability(BaseModel):
    """Web search and code execution tool support, with one entry per tool."""

    code_execution: BetaCapabilitySupport
    """
    Whether the model supports the code execution tool: true when the model supports
    at least one version of the tool, not necessarily every version.
    """

    supported: bool
    """Whether this capability is supported by the model."""

    web_search: BetaCapabilitySupport
    """
    Whether the model supports the web search tool: true when the model supports at
    least one version of the tool, not necessarily every version.
    """
