# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaManagedAgentsEffortXhigh"]


class BetaManagedAgentsEffortXhigh(BaseModel):
    """Extra-high effort. Not all models accept this level."""

    type: Literal["xhigh"]
