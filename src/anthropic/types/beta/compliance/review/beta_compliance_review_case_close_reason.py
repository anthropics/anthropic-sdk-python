from typing_extensions import Literal

from ....._models import BaseModel

__all__ = ["BetaComplianceReviewCaseCloseReason"]


class BetaComplianceReviewCaseCloseReason(BaseModel):
    """Why a review case closed."""

    type: Literal["responded", "window_ended", "ended_by_anthropic"]
    """`responded` means that Anthropic recorded a response.

    `window_ended` means that the time to respond ended with no response.
    `ended_by_anthropic` means that Anthropic ended the case before that time was
    over. New values can appear, so accept a value that you don't know.
    """
