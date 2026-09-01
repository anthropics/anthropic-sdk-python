# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Literal, Required, TypedDict

from .beta_thinking_block_binding_param import BetaThinkingBlockBindingParam

__all__ = ["BetaThinkingConfigAdaptiveParam"]


class BetaThinkingConfigAdaptiveParam(TypedDict, total=False):
    type: Required[Literal["adaptive"]]

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
