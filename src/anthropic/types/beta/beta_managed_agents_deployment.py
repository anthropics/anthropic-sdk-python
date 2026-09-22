from typing import Dict, List, Optional
from datetime import datetime
from typing_extensions import Literal

from ..._models import BaseModel
from .beta_managed_agents_schedule import BetaManagedAgentsSchedule
from .beta_managed_agents_budget_limit import BetaManagedAgentsBudgetLimit
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
    """Reference to the agent this deployment runs, resolved to a concrete version."""

    archived_at: Optional[datetime] = None
    """Time the deployment was archived. Null if not archived."""

    created_at: datetime
    """Time the deployment was created."""

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
    """Why the deployment is `paused`.

    Non-null exactly when `status` is `paused`; null otherwise.
    """

    resources: List[BetaManagedAgentsSessionResourceConfig]
    """Resources attached to sessions created from this deployment.

    Echoes the input minus write-only credentials.
    """

    schedule: Optional[BetaManagedAgentsSchedule] = None
    """Recurring cron schedule.

    Presence enables scheduled execution; null means manual-only. Includes computed
    timestamps (next fire times, last run) on the cron variant.
    """

    status: BetaManagedAgentsDeploymentStatus
    """Computed status of the deployment: `active` or `paused`.

    Archived deployments report `active` with `archived_at` set.
    """

    type: Literal["deployment"]

    updated_at: datetime
    """Time the deployment was last updated."""

    vault_ids: List[str]
    """
    Vault IDs supplying stored credentials for sessions created from this
    deployment.
    """

    budget: Optional[BetaManagedAgentsBudgetLimit] = None
    """Spend ceiling stamped onto each session created from this deployment.

    Absent when no budget is set.
    """
