# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, Optional
from typing_extensions import Literal

from ...._models import BaseModel
from .beta_session_work_data import BetaSessionWorkData

__all__ = ["BetaSelfHostedWork"]


class BetaSelfHostedWork(BaseModel):
    """Work resource representing a unit of work in a self-hosted environment.

    Work items are queued when sessions are created or when long-dormant sessions
    receive new messages. The environment worker polls for work to execute in a
    self-hosted sandbox.
    """

    id: str
    """Work identifier (e.g., 'work\\__...')"""

    acknowledged_at: Optional[str] = None
    """
    RFC 3339 timestamp when the work item was acknowledged and assigned to a
    self-hosted sandbox
    """

    created_at: str
    """RFC 3339 timestamp when work was created"""

    data: BetaSessionWorkData
    """The actual work to be performed"""

    environment_id: str
    """Environment identifier this work belongs to (e.g., `env_...`)"""

    latest_heartbeat_at: Optional[str] = None
    """RFC 3339 timestamp of the most recent heartbeat"""

    metadata: Dict[str, str]
    """User-provided metadata key-value pairs associated with this work item"""

    started_at: Optional[str] = None
    """RFC 3339 timestamp when work execution started"""

    state: Literal["queued", "starting", "active", "stopping", "stopped"]
    """Current state of the work item"""

    stop_requested_at: Optional[str] = None
    """RFC 3339 timestamp when stop was requested"""

    stopped_at: Optional[str] = None
    """RFC 3339 timestamp when work execution stopped"""

    type: Literal["work"]
    """The type of object (always 'work')"""
