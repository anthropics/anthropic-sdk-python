from datetime import datetime
from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaAvailableExternalStorageStatus"]


class BetaAvailableExternalStorageStatus(BaseModel):
    """
    The storage is verified, no Workspace has it attached, and Anthropic doesn't use
    the bucket.
    """

    healthy: bool
    """Whether the bucket passed its latest recorded check.

    It can stay `true` after the bucket stops working, so don't use it for
    monitoring.
    """

    last_checked_at: datetime
    """When the bucket's latest recorded check ran, in RFC 3339."""

    type: Literal["available"]
