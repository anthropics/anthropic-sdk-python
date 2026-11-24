from typing import Optional
from typing_extensions import Literal

from ....._models import BaseModel
from .beta_compliance_review_create_message_content import BetaComplianceReviewCreateMessageContent
from .beta_compliance_review_content_unavailable_reason import BetaComplianceReviewContentUnavailableReason

__all__ = ["BetaComplianceReviewMessageDetails"]


class BetaComplianceReviewMessageDetails(BaseModel):
    """A message sent to Claude."""

    content: Optional[BetaComplianceReviewCreateMessageContent] = None
    """The stored request and response.

    Null when `content_unavailable_reason` is set. New types can appear, so accept a
    type that you don't know.
    """

    content_unavailable_reason: Optional[BetaComplianceReviewContentUnavailableReason] = None
    """Why `content` is null.

    Null when `content` is set. New types can appear, so accept a type that you
    don't know.
    """

    model: Optional[str] = None
    """The model that the call named. Null when none was recorded."""

    type: Literal["message"]
