from datetime import datetime
from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaActiveExternalStorageStatus"]


class BetaActiveExternalStorageStatus(BaseModel):
    """At least one Workspace has the storage attached."""

    healthy: bool
    """Whether the bucket passed its latest recorded check.

    It can stay `true` after the bucket stops working, so don't use it for
    monitoring.
    """

    last_checked_at: datetime
    """When the bucket's latest recorded check ran, in RFC 3339."""

    type: Literal["active"]
