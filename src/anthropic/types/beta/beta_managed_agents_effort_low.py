# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaManagedAgentsEffortLow"]


class BetaManagedAgentsEffortLow(BaseModel):
    """Low effort. Favors latency over reasoning depth."""

    type: Literal["low"]
