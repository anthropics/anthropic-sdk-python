from .._models import BaseModel
from .effort_capability import EffortCapability
from .capability_support import CapabilitySupport
from .thinking_capability import ThinkingCapability
from .server_tools_capability import ServerToolsCapability
from .context_management_capability import ContextManagementCapability

__all__ = ["ModelCapabilities"]


class ModelCapabilities(BaseModel):
    """Model capability information."""

    batch: CapabilitySupport
    """Whether the model supports the Batch API."""

    citations: CapabilitySupport
    """Whether the model supports citation generation."""

    code_execution: CapabilitySupport
    """
    Whether code that the model runs in the code execution tool can call the
    request's other tools, as in programmatic tool calling and dynamic filtering for
    web search and web fetch. Support for the code execution tool itself is in
    `server_tools.code_execution`.
    """

    context_management: ContextManagementCapability
    """Context management support and available strategies."""

    effort: EffortCapability
    """Effort (reasoning_effort) support and available levels."""

    image_input: CapabilitySupport
    """Whether the model accepts image content blocks."""

    pdf_input: CapabilitySupport
    """Whether the model accepts PDF content blocks."""

    server_tools: ServerToolsCapability
    """Whether this model supports the web search and code execution server tools.

    `supported` is true when the model supports at least one of the tools. A
    supported tool can still be rejected for your organization, for example when an
    admin has turned web search off.
    """

    structured_outputs: CapabilitySupport
    """Whether the model supports structured output / JSON mode / strict tool schemas."""

    thinking: ThinkingCapability
    """Thinking capability and supported type configurations."""
