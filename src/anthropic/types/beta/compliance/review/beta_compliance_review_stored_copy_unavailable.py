from typing_extensions import Literal

from ....._models import BaseModel

__all__ = ["BetaComplianceReviewStoredCopyUnavailable"]


class BetaComplianceReviewStoredCopyUnavailable(BaseModel):
    """A copy of the message was stored and can't be returned."""

    type: Literal["stored_copy_unavailable"]
