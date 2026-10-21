from typing import Optional

from ..._models import BaseModel
from .beta_effort_capability import BetaEffortCapability
from .beta_capability_support import BetaCapabilitySupport
from .beta_thinking_capability import BetaThinkingCapability
from .beta_compaction_capability import BetaCompactionCapability
from .beta_server_tools_capability import BetaServerToolsCapability
from .beta_context_management_capability import BetaContextManagementCapability

__all__ = ["BetaModelCapabilities"]


class BetaModelCapabilities(BaseModel):
    """Model capability information."""

    batch: BetaCapabilitySupport
    """Whether the model supports the Batch API."""

    citations: BetaCapabilitySupport
    """Whether the model supports citation generation."""

    code_execution: BetaCapabilitySupport
    """
    Whether code that the model runs in the code execution tool can call the
    request's other tools, as in programmatic tool calling and dynamic filtering for
    web search and web fetch. Support for the code execution tool itself is in
    `server_tools.code_execution`.
    """

    compaction: Optional[BetaCompactionCapability] = None
    """
    Server-side compaction support (the top-level `compaction` parameter) and the
    accepted `compaction.type` values.
    """

    context_management: BetaContextManagementCapability
    """Context management support and available strategies."""

    effort: BetaEffortCapability
    """Effort (reasoning_effort) support and available levels."""

    image_input: BetaCapabilitySupport
    """Whether the model accepts image content blocks."""

    pdf_input: BetaCapabilitySupport
    """Whether the model accepts PDF content blocks."""

    server_tools: BetaServerToolsCapability
    """Whether this model supports the web search and code execution server tools.

    `supported` is true when the model supports at least one of the tools. A
    supported tool can still be rejected for your organization, for example when an
    admin has turned web search off.
    """

    structured_outputs: BetaCapabilitySupport
    """Whether the model supports structured output / JSON mode / strict tool schemas."""

    thinking: BetaThinkingCapability
    """Thinking capability and supported type configurations."""
