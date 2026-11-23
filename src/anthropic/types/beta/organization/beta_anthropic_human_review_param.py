from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["BetaAnthropicHumanReviewParam"]


class BetaAnthropicHumanReviewParam(TypedDict, total=False):
    """
    Whether Anthropic's human review applies to the Workspace's inference
    data.
    """

    type: Required[Literal["disabled", "enabled"]]
