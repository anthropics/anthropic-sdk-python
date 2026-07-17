# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaManagedAgentsSessionRetriesExhausted"]


class BetaManagedAgentsSessionRetriesExhausted(BaseModel):
    """
    The turn ended because repeated errors exhausted the automatic retry budget or the agent reached an internal execution limit.
    """

    type: Literal["retries_exhausted"]
