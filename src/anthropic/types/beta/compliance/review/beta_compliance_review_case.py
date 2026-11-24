from typing import List, Optional
from datetime import datetime
from typing_extensions import Literal

from ....._models import BaseModel
from .beta_compliance_review_transcript import BetaComplianceReviewTranscript
from .beta_compliance_review_case_status import BetaComplianceReviewCaseStatus
from .beta_compliance_review_policy_category import BetaComplianceReviewPolicyCategory
from .beta_compliance_review_enforcement_action import BetaComplianceReviewEnforcementAction

__all__ = ["BetaComplianceReviewCase"]


class BetaComplianceReviewCase(BaseModel):
    """
    A record of an organization's messages that Anthropic flagged and sent to the organization to review. It lists the messages by ID and doesn't include their content.
    """

    id: str
    """The unique ID of the case (`rvc_...`)."""

    created_at: datetime
    """When Anthropic sent the case. The time you have to respond starts here."""

    enforcement_action: Optional[BetaComplianceReviewEnforcementAction] = None
    """The action that Anthropic took before it sent the case. Null when it took none."""

    organization_id: str
    """
    The UUID of the organization that sent the flagged messages, which the case
    belongs to.
    """

    policy_categories: List[BetaComplianceReviewPolicyCategory]
    """Anthropic's labels for why the messages were flagged, such as `cyber` or
    `fraud`.

    There is at least one. New values can appear, so accept a value that you don't
    know.
    """

    status: BetaComplianceReviewCaseStatus
    """Whether Anthropic is still waiting for a response."""

    transcripts: List[BetaComplianceReviewTranscript]
    """The flagged messages. There is at least one, and the list isn't paginated."""

    type: Literal["compliance_review_case"]
    """The object type, always `compliance_review_case`."""

    updated_at: datetime
    """When the case last changed.

    It changes when Anthropic sends the case, when the case closes, and when
    Anthropic sends a notice about the case.
    """

    workspace_id: Optional[str] = None
    """The ID of the workspace that sent the flagged messages (`wrkspc_...`).

    Null when the messages have no workspace, and it can be null for the default
    workspace.
    """
