from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaManagedAgentsSessionRetriesExhausted"]


class BetaManagedAgentsSessionRetriesExhausted(BaseModel):
    """
    The turn ended because repeated errors exhausted the retry budget or an error escalated to `retry_status: 'exhausted'`.
    """

    type: Literal["retries_exhausted"]
