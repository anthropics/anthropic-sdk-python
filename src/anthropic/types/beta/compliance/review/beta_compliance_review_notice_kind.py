from typing_extensions import Literal

from ....._models import BaseModel

__all__ = ["BetaComplianceReviewNoticeKind"]


class BetaComplianceReviewNoticeKind(BaseModel):
    """The kind of a review notice."""

    type: Literal["response_requested", "warning", "question"]
    """`response_requested` asks you to respond to the cases in `case_ids`.

    For `warning` and `question`, `message` explains how to answer if an answer is
    needed. New values can appear, so accept a value that you don't know.
    """
