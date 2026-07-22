# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaManagedAgentsEffortHigh"]


class BetaManagedAgentsEffortHigh(BaseModel):
    """High effort. Favors reasoning depth."""

    type: Literal["high"]
