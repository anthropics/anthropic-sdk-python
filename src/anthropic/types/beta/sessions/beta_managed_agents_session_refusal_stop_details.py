from typing import Optional
from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaManagedAgentsSessionRefusalStopDetails"]


class BetaManagedAgentsSessionRefusalStopDetails(BaseModel):
    """Structured information about a refusal."""

    category: Optional[Literal["cyber", "bio", "frontier_llm", "reasoning_extraction", "general_harms"]] = None
    """
    The policy category that triggered the refusal, or `null` when there is no named
    category. New values can be added over time.
    """

    explanation: Optional[str] = None
    """Human-readable explanation of the refusal, or `null` when none is available.

    The wording can change, so do not parse it.
    """

    type: Literal["refusal"]
