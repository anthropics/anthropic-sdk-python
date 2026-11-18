from typing import Optional
from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaWorkLeaseState"]


class BetaWorkLeaseState(BaseModel):
    """A work item's lease as the server holds it."""

    last_heartbeat: Optional[str] = None
    """RFC 3339 timestamp of the stored heartbeat, or null if there has been none"""

    lease_extended: bool
    """Always false: a refused heartbeat does not extend the lease"""

    state: Literal["queued", "starting", "active", "stopping", "stopped"]
    """Current state of the work item"""

    ttl_seconds: int
    """TTL of the lease"""
