# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Optional
from datetime import datetime
from typing_extensions import Literal

from ..._models import BaseModel
from .beta_managed_agents_schedule import BetaManagedAgentsSchedule
from .beta_managed_agents_agent_reference import BetaManagedAgentsAgentReference
from .beta_managed_agents_deployment_status import BetaManagedAgentsDeploymentStatus
from .beta_managed_agents_session_resource_config import BetaManagedAgentsSessionResourceConfig
from .beta_managed_agents_deployment_initial_event import BetaManagedAgentsDeploymentInitialEvent
from .beta_managed_agents_deployment_paused_reason import BetaManagedAgentsDeploymentPausedReason

__all__ = ["BetaManagedAgentsDeployment"]


class BetaManagedAgentsDeployment(BaseModel):
    """
    A deployment is a configured instance of an agent — it binds the agent to everything needed to run it autonomously: an environment, credentials, initial events, and an optional schedule.
    """

    id: str
    """Unique identifier for this deployment."""

    agent: BetaManagedAgentsAgentReference
    """A resolved agent reference with a concrete version."""

    archived_at: Optional[datetime] = None
    """A timestamp in RFC 3339 format"""

    created_at: datetime
    """A timestamp in RFC 3339 format"""

    description: Optional[str] = None
    """Description of what the deployment does."""

    environment_id: str
    """ID of the `environment` where sessions run."""

    initial_events: List[BetaManagedAgentsDeploymentInitialEvent]
    """Events sent to each session immediately after creation."""

    metadata: Dict[str, str]
    """Arbitrary key-value metadata. Maximum 16 pairs."""

    name: str
    """Human-readable name."""

    paused_reason: Optional[BetaManagedAgentsDeploymentPausedReason] = None
    """Why a deployment is paused. Non-null exactly when `status` is `paused`."""

    resources: List[BetaManagedAgentsSessionResourceConfig]
    """Resources attached to sessions created from this deployment.

    Echoes the input minus write-only credentials.
    """

    schedule: Optional[BetaManagedAgentsSchedule] = None
    """5-field POSIX cron schedule with computed runtime timestamps."""

    status: BetaManagedAgentsDeploymentStatus
    """Lifecycle status of a deployment."""

    type: Literal["deployment"]

    updated_at: datetime
    """A timestamp in RFC 3339 format"""

    vault_ids: List[str]
    """
    Vault IDs supplying stored credentials for sessions created from this
    deployment.
    """
