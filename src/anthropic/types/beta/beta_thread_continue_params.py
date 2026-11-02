from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["BetaThreadContinueParams"]


class BetaThreadContinueParams(TypedDict, total=False):
    """Resume from the response named by ``previous_message_id``."""

    previous_message_id: Required[str]
    """The `id` of the previous response in this Thread."""

    type: Required[Literal["continue"]]
