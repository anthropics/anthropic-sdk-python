# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["BetaOutputBehaviorUpdateExistingParam"]


class BetaOutputBehaviorUpdateExistingParam(TypedDict, total=False):
    """
    The job writes the consolidated memories into this existing memory store instead of creating one. In EAP the store must be the job's own memory_store input, so the job consolidates the store in place.
    """

    memory_store_id: Required[str]

    type: Required[Literal["update_existing"]]
