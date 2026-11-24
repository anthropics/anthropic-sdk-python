from typing import List, Optional
from datetime import datetime
from typing_extensions import Literal

from ....._models import BaseModel
from .beta_compliance_review_notice_kind import BetaComplianceReviewNoticeKind

__all__ = ["BetaComplianceReviewNotice"]


class BetaComplianceReviewNotice(BaseModel):
    """
    A message from Anthropic to an organization about its review cases or about the organization as a whole, such as a request to respond by a date, a warning, or a question. A notice doesn't change after Anthropic sends it.
    """

    id: str
    """The unique ID of the notice (`rvn_...`)."""

    case_ids: List[str]
    """The IDs of the cases that the notice is about (`rvc_...`).

    Empty when the notice is about the whole organization.
    """

    created_at: datetime
    """When Anthropic sent the notice."""

    kind: BetaComplianceReviewNoticeKind
    """What kind of notice this is."""

    message: str
    """The text of the notice."""

    organization_id: str
    """The UUID of the organization that the notice is for."""

    respond_by: Optional[datetime] = None
    """The time by which Anthropic asks for an answer.

    Null when there is no deadline. Missing it changes nothing on a case, and the
    time to respond to a case can end before it.
    """

    type: Literal["compliance_review_notice"]
    """The object type, always `compliance_review_notice`."""
