from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaOutputBehaviorUpdateExisting"]


class BetaOutputBehaviorUpdateExisting(BaseModel):
    """
    The job writes the consolidated memories into this existing memory store instead of creating one. In EAP the store must be the job's own memory_store input, so the job consolidates the store in place.
    """

    memory_store_id: str
    """The ID of the memory store for the dream to write its result to
    (`memstore_...`).

    It must be the memory store in the `memory_store` entry of `inputs`.
    """

    type: Literal["update_existing"]
