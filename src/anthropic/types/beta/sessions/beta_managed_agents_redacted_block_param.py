from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["BetaManagedAgentsRedactedBlockParam"]


class BetaManagedAgentsRedactedBlockParam(TypedDict, total=False):
    """Placeholder for content withheld by Anthropic model policy."""

    type: Required[Literal["redacted"]]
