# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaDreamMemoryStoreInput"]


class BetaDreamMemoryStoreInput(BaseModel):
    """An input memory store the dream reads from.

    The dream never mutates this store unless it is also the destination: with output_behavior {type: "update_existing"} the job consolidates this store in place.
    """

    memory_store_id: str

    type: Literal["memory_store"]
