# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaSelfHostedWorkHeartbeatResponse"]


class BetaSelfHostedWorkHeartbeatResponse(BaseModel):
    """Response after recording a heartbeat for a work item."""

    last_heartbeat: str
    """RFC 3339 timestamp of the actual heartbeat from DB"""

    lease_extended: bool
    """Whether the heartbeat succeeded in extending the lease"""

    state: Literal["queued", "starting", "active", "stopping", "stopped"]
    """Current state of the work item (active/stopping/stopped)"""

    ttl_seconds: int
    """Effective TTL applied to the lease"""

    type: Literal["work_heartbeat"]
    """The type of response"""
