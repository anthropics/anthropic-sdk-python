# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import Literal

from ..._models import BaseModel
from .beta_container import BetaContainer
from .beta_stop_reason import BetaStopReason
from .beta_message_delta_usage import BetaMessageDeltaUsage
from .beta_refusal_stop_details import BetaRefusalStopDetails
from .beta_context_management_response import BetaContextManagementResponse
from .beta_thinking_dropped_input_transformation import BetaThinkingDroppedInputTransformation

__all__ = ["BetaRawMessageDeltaEvent", "Delta"]


class Delta(BaseModel):
    container: Optional[BetaContainer] = None
    """
    Information about the container used in the request (for the code execution
    tool)
    """

    stop_details: Optional[BetaRefusalStopDetails] = None
    """Structured information about a refusal."""

    stop_reason: Optional[BetaStopReason] = None

    stop_sequence: Optional[str] = None


class BetaRawMessageDeltaEvent(BaseModel):
    context_management: Optional[BetaContextManagementResponse] = None
    """Information about context management strategies applied during the request"""

    delta: Delta

    type: Literal["message_delta"]

    usage: BetaMessageDeltaUsage
    """Billing and rate-limit usage.

    Anthropic's API bills and rate-limits by token counts, as tokens represent the
    underlying cost to our systems.

    Under the hood, the API transforms requests into a format suitable for the
    model. The model's output then goes through a parsing stage before becoming an
    API response. As a result, the token counts in `usage` will not match one-to-one
    with the exact visible content of an API request or response.

    For example, `output_tokens` will be non-zero, even for an empty string response
    from Claude.

    Total input tokens in a request is the summation of `input_tokens`,
    `cache_creation_input_tokens`, and `cache_read_input_tokens`.
    """

    input_transformations: Optional[List[BetaThinkingDroppedInputTransformation]] = None
    """
    Changes the API made to the request's input before showing it to the model: one
    entry per change, in request order. Today the only entry type is
    `thinking_dropped` — a `thinking`, `redacted_thinking` or `connector_text` block
    from the request's `messages` that was removed from the prompt instead of being
    shown to the model because it failed a binding check. More entry types may be
    added over time; ignore types you do not recognize.

    Requires `anthropic-beta: thinking-binding-controls-2026-08-01`. Present on
    every such response from a model that supports extended thinking, as `[]` when
    nothing was changed; without the beta, blocks are removed all the same but
    nothing is reported. Removed blocks contribute nothing to `usage.input_tokens`.
    When streaming, the array is final in `message_start`; the final `message_delta`
    event carries it only when a server-side model fallback happened mid-stream, in
    which case it holds the serving model's entries and replaces the one in
    `message_start`.
    """
