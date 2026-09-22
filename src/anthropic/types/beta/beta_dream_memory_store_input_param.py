from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["BetaDreamMemoryStoreInputParam"]


class BetaDreamMemoryStoreInputParam(TypedDict, total=False):
    """The memory store that a dream reads, given as an entry in `inputs`.

    With `output_behavior` set to `update_existing`, the dream writes its result into this memory store. Otherwise the dream doesn't change it.
    """

    memory_store_id: Required[str]
    """The ID of the memory store for the dream to read (`memstore_...`).

    The memory store must be in the same workspace as the dream and must not be
    archived.
    """

    type: Required[Literal["memory_store"]]
