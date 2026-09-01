# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import TypedDict

from .beta_thinking_prefix_mismatch_behavior import BetaThinkingPrefixMismatchBehavior

__all__ = ["BetaThinkingBlockBindingParam"]


class BetaThinkingBlockBindingParam(TypedDict, total=False):
    """
    Controls for block binding: what happens when a thinking block this
    request sends back fails the conversation check. Every field is optional;
    an empty object means every default.
    """

    prefix_mismatch_behavior: Optional[BetaThinkingPrefixMismatchBehavior]
    """
    What happens when a thinking block in `messages` fails the conversation check:
    it was created in a different conversation, or the messages before it have
    changed since. `"error"` (the default) fails the request with a 400 error.
    `"drop_block"` removes the failing blocks and the request proceeds; the model no
    longer sees the dropped reasoning.
    """
