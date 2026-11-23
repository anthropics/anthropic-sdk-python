from __future__ import annotations

from typing_extensions import TypedDict

from .beta_storage_member_param import BetaStorageMemberParam
from .beta_anthropic_human_review_param import BetaAnthropicHumanReviewParam

__all__ = ["BetaInferenceDataPrivacyCreateParam"]


class BetaInferenceDataPrivacyCreateParam(TypedDict, total=False):
    """
    Where the Workspace's retained inference data and transcript copies go, and
    whether Anthropic's human review applies. A member cannot be null; omit it
    instead.
    """

    human_review: BetaAnthropicHumanReviewParam
    """Whether Anthropic's human review applies to the Workspace.

    `disabled` needs Anthropic's approval. When omitted, `enabled`. Cannot be null.
    """

    safeguards_storage: BetaStorageMemberParam
    """Where the data Anthropic's safeguards systems retain for the Workspace goes.

    `external` sends it, once the attach takes effect, to the External Storage that
    `external_storage_id` names. `internal` means no External Storage: it goes to
    Anthropic's storage or, on a cloud provider's platform, to that provider's
    storage. When omitted, `internal`. Cannot be null.
    """

    transcripts_storage: BetaStorageMemberParam
    """
    Where copies of the Workspace's transcripts and its cases (Anthropic's safety
    findings about those transcripts) go. `external` sends them, once the attach
    takes effect, to the External Storage that `external_storage_id` names.
    `internal` means no External Storage, so no copies are made. When omitted,
    `internal`. Cannot be null.
    """
