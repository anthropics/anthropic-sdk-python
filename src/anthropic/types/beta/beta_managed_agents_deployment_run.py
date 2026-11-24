from typing import Union, Optional
from datetime import datetime
from typing_extensions import Literal, Annotated, TypeAlias

from ..._models import BaseModel, UnionDiscriminator
from .beta_managed_agents_agent_reference import BetaManagedAgentsAgentReference
from .beta_managed_agents_trigger_context import BetaManagedAgentsTriggerContext
from .beta_managed_agents_unknown_run_error_object import BetaManagedAgentsUnknownRunErrorObject
from .beta_managed_agents_agent_archived_run_error_object import BetaManagedAgentsAgentArchivedRunErrorObject
from .beta_managed_agents_file_not_found_run_error_object import BetaManagedAgentsFileNotFoundRunErrorObject
from .beta_managed_agents_vault_archived_run_error_object import BetaManagedAgentsVaultArchivedRunErrorObject
from .beta_managed_agents_skill_not_found_run_error_object import BetaManagedAgentsSkillNotFoundRunErrorObject
from .beta_managed_agents_vault_not_found_run_error_object import BetaManagedAgentsVaultNotFoundRunErrorObject
from .beta_managed_agents_mcp_egress_blocked_run_error_object import BetaManagedAgentsMCPEgressBlockedRunErrorObject
from .beta_managed_agents_workspace_archived_run_error_object import BetaManagedAgentsWorkspaceArchivedRunErrorObject
from .beta_managed_agents_environment_archived_run_error_object import (
    BetaManagedAgentsEnvironmentArchivedRunErrorObject,
)
from .beta_managed_agents_session_rate_limited_run_error_object import BetaManagedAgentsSessionRateLimitedRunErrorObject
from .beta_managed_agents_environment_not_found_run_error_object import (
    BetaManagedAgentsEnvironmentNotFoundRunErrorObject,
)
from .beta_managed_agents_memory_store_archived_run_error_object import (
    BetaManagedAgentsMemoryStoreArchivedRunErrorObject,
)
from .beta_managed_agents_organization_disabled_run_error_object import (
    BetaManagedAgentsOrganizationDisabledRunErrorObject,
)
from .beta_managed_agents_session_creation_rejected_run_error_object import (
    BetaManagedAgentsSessionCreationRejectedRunErrorObject,
)
from .beta_managed_agents_session_resource_not_found_run_error_object import (
    BetaManagedAgentsSessionResourceNotFoundRunErrorObject,
)
from .beta_managed_agents_self_hosted_resources_unsupported_run_error_object import (
    BetaManagedAgentsSelfHostedResourcesUnsupportedRunErrorObject,
)

__all__ = ["BetaManagedAgentsDeploymentRun", "Error"]

Error: TypeAlias = Annotated[
    Union[
        BetaManagedAgentsEnvironmentArchivedRunErrorObject,
        BetaManagedAgentsAgentArchivedRunErrorObject,
        BetaManagedAgentsEnvironmentNotFoundRunErrorObject,
        BetaManagedAgentsVaultNotFoundRunErrorObject,
        BetaManagedAgentsVaultArchivedRunErrorObject,
        BetaManagedAgentsFileNotFoundRunErrorObject,
        BetaManagedAgentsMemoryStoreArchivedRunErrorObject,
        BetaManagedAgentsSkillNotFoundRunErrorObject,
        BetaManagedAgentsSessionResourceNotFoundRunErrorObject,
        BetaManagedAgentsWorkspaceArchivedRunErrorObject,
        BetaManagedAgentsOrganizationDisabledRunErrorObject,
        BetaManagedAgentsSessionRateLimitedRunErrorObject,
        BetaManagedAgentsSessionCreationRejectedRunErrorObject,
        BetaManagedAgentsUnknownRunErrorObject,
        BetaManagedAgentsSelfHostedResourcesUnsupportedRunErrorObject,
        BetaManagedAgentsMCPEgressBlockedRunErrorObject,
        None,
    ],
    UnionDiscriminator("type"),
]
"""Populated on creation failure.

Null on success. Exactly one of `session_id` or `error` is non-null.
"""


class BetaManagedAgentsDeploymentRun(BaseModel):
    """A persistent, append-only record of a single deployment execution.

    Records session creation success or failure — no session lifecycle tracking.
    """

    id: str
    """Unique identifier for this run (`drun_...`)."""

    agent: BetaManagedAgentsAgentReference
    """Snapshot of the agent at fire time.

    Always fully resolved — deployments pin agent + version.
    """

    created_at: datetime
    """Time this run record was persisted."""

    deployment_id: str
    """ID of the deployment that produced this run."""

    error: Optional[Error] = None
    """Populated on creation failure.

    Null on success. Exactly one of `session_id` or `error` is non-null.
    """

    session_id: Optional[str] = None
    """Populated on success.

    Null on creation failure. Exactly one of `session_id` or `error` is non-null.
    """

    trigger_context: BetaManagedAgentsTriggerContext
    """What triggered this run and trigger-specific metadata."""

    type: Literal["deployment_run"]
