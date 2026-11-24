from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["BetaStorageNotApprovedErrorDetails"]


class BetaStorageNotApprovedErrorDetails(BaseModel):
    """
    Anthropic has not approved keeping data in a customer-owned storage bucket for the organization, project or user profile this request applies to, or has paused or withdrawn its approval. If you did not expect this, contact Anthropic.
    """

    error_code: Literal["storage_not_approved"]
