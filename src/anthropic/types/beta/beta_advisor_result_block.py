# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaAdvisorResultBlock"]


class BetaAdvisorResultBlock(BaseModel):
    stop_reason: Optional[str] = None
    """
    The advisor sub-inference's stop reason (same values as the top-level message
    `stop_reason`). `max_tokens` indicates the advisor's output was truncated at the
    tool's `max_tokens` value or the advisor model's policy cap.
    """

    text: str

    type: Literal["advisor_result"]
