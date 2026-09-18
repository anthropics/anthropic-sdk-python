from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaOutputBehaviorUpdateExisting"]


class BetaOutputBehaviorUpdateExisting(BaseModel):
    """Write the result into the input memory store instead of a new memory store.

    The credential must be allowed to write memory stores, or the request returns a 403 error. While another `update_existing` dream on the same memory store hasn't fully stopped, the request returns a 409 error.
    """

    memory_store_id: str
    """The ID of the memory store for the dream to write its result to
    (`memstore_...`).

    It must be the memory store in the `memory_store` entry of `inputs`.
    """

    type: Literal["update_existing"]
