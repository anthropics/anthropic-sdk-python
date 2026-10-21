from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["BetaOutputBehaviorUpdateExistingParam"]


class BetaOutputBehaviorUpdateExistingParam(TypedDict, total=False):
    """Write the result into the input memory store instead of a new memory store.

    The credential must be allowed to write memory stores, or the request returns a 403 error. While another `update_existing` dream on the same memory store hasn't fully stopped, the request returns a 409 error.
    """

    memory_store_id: Required[str]
    """The ID of the memory store for the dream to write its result to
    (`memstore_...`).

    It must be the memory store in the `memory_store` entry of `inputs`.
    """

    type: Required[Literal["update_existing"]]
