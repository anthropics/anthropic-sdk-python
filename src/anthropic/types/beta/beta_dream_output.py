from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaDreamOutput"]


class BetaDreamOutput(BaseModel):
    """The memory store that holds a dream's result, as an entry in `outputs`."""

    memory_store_id: str
    """The ID of the memory store that the dream writes its result to (`memstore_...`).

    With `output_behavior` set to `create_new`, this is a new memory store. With
    `update_existing`, it is the input memory store.
    """

    type: Literal["memory_store"]
