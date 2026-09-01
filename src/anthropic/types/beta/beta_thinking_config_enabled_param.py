# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Literal, Required, TypedDict

from .beta_thinking_block_binding_param import BetaThinkingBlockBindingParam

__all__ = ["BetaThinkingConfigEnabledParam"]


class BetaThinkingConfigEnabledParam(TypedDict, total=False):
    budget_tokens: Required[int]
    """Determines how many tokens Claude can use for its internal reasoning process.

    Larger budgets can enable more thorough analysis for complex problems, improving
    response quality.

    Must be ≥1024 and less than `max_tokens`.

    See
    [extended thinking](https://platform.claude.com/docs/en/build-with-claude/extended-thinking)
    for details.
    """

    type: Required[Literal["enabled"]]

    block_binding: Optional[BetaThinkingBlockBindingParam]
    """
    Controls for block binding: what happens when a thinking block this request
    sends back fails the conversation check. Every field is optional; an empty
    object means every default.
    """

    display: Optional[Literal["summarized", "omitted", "updates"]]
    """Controls how thinking content appears in the response.

    When set to `summarized`, thinking is returned normally. When set to `omitted`,
    thinking content is redacted but a signature is returned for multi-turn
    continuity. Defaults to `summarized`.
    """
