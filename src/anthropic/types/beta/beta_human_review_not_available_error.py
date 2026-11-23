from typing_extensions import Literal

from ..._exceptions import BadRequestError
from .beta_human_review_not_available_error_details import BetaHumanReviewNotAvailableErrorDetails

__all__ = ["BetaHumanReviewNotAvailableError"]


class BetaHumanReviewNotAvailableError(BadRequestError):
    """
    Human review can't be set as requested on this Workspace, so the request changed nothing. The error's `message` says what to do instead.
    """

    error_code: Literal["human_review_not_available"]  # pyright: ignore[reportIncompatibleVariableOverride]
    details: BetaHumanReviewNotAvailableErrorDetails  # pyright: ignore[reportIncompatibleVariableOverride]
