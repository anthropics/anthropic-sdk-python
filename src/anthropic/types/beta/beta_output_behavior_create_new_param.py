# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["BetaOutputBehaviorCreateNewParam"]


class BetaOutputBehaviorCreateNewParam(TypedDict, total=False):
    """
    The default destination: the job creates a new output memory store as a clone of the memory_store input and writes the consolidated memories into it. The input store is never mutated.
    """

    type: Required[Literal["create_new"]]
