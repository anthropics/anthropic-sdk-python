from datetime import datetime
from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaDrainingExternalStorageStatus"]


class BetaDrainingExternalStorageStatus(BaseModel):
    """No Workspace has the storage attached.

    A Workspace can attach it again, unless
    `removal_started` is true.
    """

    healthy: bool
    """Whether the bucket passed its latest recorded check.

    It can stay `true` after the bucket stops working, so don't use it for
    monitoring.
    """

    last_checked_at: datetime
    """When the bucket's latest recorded check ran, in RFC 3339."""

    removal_started: bool
    """True once a delete has started removing this storage, which can't be undone.

    It then can't be attached, and another delete finishes the removal.
    """

    type: Literal["draining"]
