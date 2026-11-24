from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["BetaCMEKNotApprovedErrorDetails"]


class BetaCMEKNotApprovedErrorDetails(BaseModel):
    """
    Anthropic has not approved customer-managed encryption keys for the organization, project or user profile this request applies to, or has paused or withdrawn its approval. If you did not expect this, contact Anthropic.
    """

    error_code: Literal["cmek_not_approved"]
