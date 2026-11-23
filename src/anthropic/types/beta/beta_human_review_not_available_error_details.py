from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaHumanReviewNotAvailableErrorDetails"]


class BetaHumanReviewNotAvailableErrorDetails(BaseModel):
    """
    Human review can't be set as requested on this Workspace, so the request changed nothing. The error's `message` says what to do instead.
    """

    error_code: Literal["human_review_not_available"]
