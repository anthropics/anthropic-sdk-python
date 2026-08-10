# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaOutputBehaviorCreateNew"]


class BetaOutputBehaviorCreateNew(BaseModel):
    """
    The default destination: the job creates a new output memory store as a clone of the memory_store input and writes the consolidated memories into it. The input store is never mutated.
    """

    type: Literal["create_new"]
