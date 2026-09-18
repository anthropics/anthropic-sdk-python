from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaDreamMemoryStoreInput"]


class BetaDreamMemoryStoreInput(BaseModel):
    """An input memory store the dream reads from.

    The dream never mutates this store unless it is also the destination: with output_behavior {type: "update_existing"} the job consolidates this store in place.
    """

    memory_store_id: str
    """The ID of the memory store for the dream to read (`memstore_...`).

    The memory store must be in the same workspace as the dream and must not be
    archived.
    """

    type: Literal["memory_store"]
