from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaDreamMemoryStoreInput"]


class BetaDreamMemoryStoreInput(BaseModel):
    """The memory store that a dream reads, given as an entry in `inputs`.

    With `output_behavior` set to `update_existing`, the dream writes its result into this memory store. Otherwise the dream doesn't change it.
    """

    memory_store_id: str
    """The ID of the memory store for the dream to read (`memstore_...`).

    The memory store must be in the same workspace as the dream and must not be
    archived.
    """

    type: Literal["memory_store"]
