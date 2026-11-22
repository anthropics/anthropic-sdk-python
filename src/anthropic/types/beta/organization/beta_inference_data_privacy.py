from typing import Optional

from ...._models import BaseModel
from .beta_storage_member import BetaStorageMember
from .beta_anthropic_human_review import BetaAnthropicHumanReview

__all__ = ["BetaInferenceDataPrivacy"]


class BetaInferenceDataPrivacy(BaseModel):
    human_review: Optional[BetaAnthropicHumanReview] = None
    """The Workspace's human review setting.

    Human review is off only while this is `disabled` and Anthropic's approval
    stands.
    """

    safeguards_storage: Optional[BetaStorageMember] = None
    """Where the data Anthropic's safeguards systems retain for the Workspace goes.

    `external` sends it to the External Storage that `external_storage_id` names.
    `internal` means no External Storage: it goes to Anthropic's storage or, on a
    cloud provider's platform, to that provider's storage. A recent change may not
    have taken effect yet.
    """

    transcripts_storage: Optional[BetaStorageMember] = None
    """
    Where copies of the Workspace's transcripts and its cases (Anthropic's safety
    findings about those transcripts) go. `external` sends them to the External
    Storage that `external_storage_id` names. `internal` means no External Storage,
    so no copies are made. A recent change may not have taken effect yet.
    """
