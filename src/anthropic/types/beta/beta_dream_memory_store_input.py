# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaDreamMemoryStoreInput"]


class BetaDreamMemoryStoreInput(BaseModel):
    """An input memory store the dream reads from. The dream never mutates this store."""

    memory_store_id: str

    type: Literal["memory_store"]
