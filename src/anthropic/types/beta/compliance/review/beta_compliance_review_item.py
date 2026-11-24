from typing import Optional
from datetime import datetime
from typing_extensions import Literal

from ....._models import BaseModel
from .beta_compliance_review_actor import BetaComplianceReviewActor
from .beta_compliance_review_message_details import BetaComplianceReviewMessageDetails
from .beta_compliance_review_safeguards_reason import BetaComplianceReviewSafeguardsReason

__all__ = ["BetaComplianceReviewItem"]


class BetaComplianceReviewItem(BaseModel):
    """One stored item that the organization it belongs to can read for review."""

    id: str
    """The ID of the item. For a message, its own ID, such as `msg_...`."""

    actor: Optional[BetaComplianceReviewActor] = None
    """For a message, who sent it.

    Null when no sender was recorded. New types can appear, so accept a type that
    you don't know.
    """

    content_expires_at: datetime
    """Read the item, and save any copy you need, by this time.

    The item can stop being readable sooner.
    """

    created_at: datetime
    """For a message, when Anthropic received the call."""

    details: BetaComplianceReviewMessageDetails
    """What is particular to this kind of item.

    New types can appear, so accept a type that you don't know.
    """

    organization_id: str
    """The UUID of the organization that the item belongs to.

    For a message, the organization that sent it.
    """

    read_reason: BetaComplianceReviewSafeguardsReason
    """Why the item is readable.

    New types can appear, so accept a type that you don't know.
    """

    type: Literal["compliance_review_item"]
    """The object type, always `compliance_review_item`."""

    user_profile_id: Optional[str] = None
    """The ID of the user profile that the item was attributed to (`uprof_...`).

    Null when none was recorded.
    """

    workspace_id: Optional[str] = None
    """The ID of the workspace (`wrkspc_...`).

    Null when the item isn't attributed to a workspace.
    """
