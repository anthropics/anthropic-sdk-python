from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["BetaOutputBehaviorCreateNewParam"]


class BetaOutputBehaviorCreateNewParam(TypedDict, total=False):
    """
    Write the result to a new memory store that starts as a copy of the input memory store. This is the default.

    The new memory store is in the same workspace as the dream. The dream doesn't change the input memory store.
    """

    type: Required[Literal["create_new"]]
