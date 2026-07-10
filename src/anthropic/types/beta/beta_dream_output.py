# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaDreamOutput"]


class BetaDreamOutput(BaseModel):
    """An output memory store the dream writes consolidated memories into."""

    memory_store_id: str

    type: Literal["memory_store"]
