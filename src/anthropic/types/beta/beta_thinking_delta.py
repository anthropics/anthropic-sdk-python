# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaThinkingDelta"]


class BetaThinkingDelta(BaseModel):
    estimated_tokens: Optional[int] = None
    """
    Per-frame increment of a coarse, running estimate of the tokens this thinking
    block has produced so far. Present whenever the
    `thinking-token-count-2026-05-13` beta is set; `null` unless `thinking.display`
    resolves to `"omitted"` and a count is due this frame. Sum the increments across
    `thinking_delta` frames on this block for a progress indicator. Each increment
    is a non-negative multiple of a fixed quantum and the cadence is rate-limited,
    so this is a deliberately lossy display hint, not a billable count;
    `usage.output_tokens` remains authoritative.
    """

    thinking: str

    type: Literal["thinking_delta"]
