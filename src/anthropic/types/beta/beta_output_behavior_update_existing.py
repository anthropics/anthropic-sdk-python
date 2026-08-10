# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaOutputBehaviorUpdateExisting"]


class BetaOutputBehaviorUpdateExisting(BaseModel):
    """
    The job writes the consolidated memories into this existing memory store instead of creating one. In EAP the store must be the job's own memory_store input, so the job consolidates the store in place.
    """

    memory_store_id: str

    type: Literal["update_existing"]
