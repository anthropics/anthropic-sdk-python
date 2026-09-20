from typing import List, Optional
from typing_extensions import Literal

from ..model import Model
from ..._models import BaseModel
from .beta_cache_control_ephemeral import BetaCacheControlEphemeral

__all__ = ["BetaAdvisorTool20260301"]


class BetaAdvisorTool20260301(BaseModel):
    model: Model
    """The model that will complete your prompt.

    See [models](https://docs.anthropic.com/en/docs/models-overview) for additional
    details and options.
    """

    name: Literal["advisor"]
    """Name of the tool.

    This is how the tool will be called by the model and in `tool_use` blocks.
    """

    type: Literal["advisor_20260301"]

    allowed_callers: Optional[
        List[Literal["direct", "code_execution_20250825", "code_execution_20260120", "code_execution_20260521"]]
    ] = None

    cache_control: Optional[BetaCacheControlEphemeral] = None
    """Create a cache control breakpoint at this content block."""

    caching: Optional[BetaCacheControlEphemeral] = None
    """Caching for the advisor's own prompt.

    When set, each advisor call writes a cache entry at the given TTL so subsequent
    calls in the same conversation read the stable prefix. When omitted, the advisor
    prompt is not cached.
    """

    defer_loading: Optional[bool] = None
    """If true, tool will not be included in initial system prompt.

    Only loaded when returned via tool_reference from tool search.
    """

    max_tokens: Optional[int] = None
    """Bounds the advisor's total output (thinking + text) per call.

    When the advisor hits this cap, the returned advisor_result or
    advisor_redacted_result block carries stop_reason='max_tokens', and a truncation
    note is appended to the advice text the worker model sees (inside the encrypted
    blob in redacted mode). When set, the server also emits a remaining-tokens
    budget block in the advisor's prompt so the advisor self-shapes toward the cap.
    When omitted, the advisor model's default output cap applies and no budget block
    is emitted.
    """

    max_uses: Optional[int] = None
    """Maximum number of times the tool can be used in the API request."""

    strict: Optional[bool] = None
    """When true, guarantees schema validation on tool names and inputs"""
