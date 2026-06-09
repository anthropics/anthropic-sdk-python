# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Union, Optional
from datetime import datetime
from typing_extensions import Literal, Annotated, TypeAlias

from ..._utils import PropertyInfo
from ..._models import BaseModel
from .beta_managed_agents_agent_reference import BetaManagedAgentsAgentReference
from .beta_managed_agents_trigger_context import BetaManagedAgentsTriggerContext
from .beta_managed_agents_unknown_run_error import BetaManagedAgentsUnknownRunError
from .beta_managed_agents_agent_archived_run_error import BetaManagedAgentsAgentArchivedRunError
from .beta_managed_agents_file_not_found_run_error import BetaManagedAgentsFileNotFoundRunError
from .beta_managed_agents_vault_archived_run_error import BetaManagedAgentsVaultArchivedRunError
from .beta_managed_agents_skill_not_found_run_error import BetaManagedAgentsSkillNotFoundRunError
from .beta_managed_agents_vault_not_found_run_error import BetaManagedAgentsVaultNotFoundRunError
from .beta_managed_agents_mcp_egress_blocked_run_error import BetaManagedAgentsMCPEgressBlockedRunError
from .beta_managed_agents_workspace_archived_run_error import BetaManagedAgentsWorkspaceArchivedRunError
from .beta_managed_agents_environment_archived_run_error import BetaManagedAgentsEnvironmentArchivedRunError
from .beta_managed_agents_session_rate_limited_run_error import BetaManagedAgentsSessionRateLimitedRunError
from .beta_managed_agents_environment_not_found_run_error import BetaManagedAgentsEnvironmentNotFoundRunError
from .beta_managed_agents_memory_store_archived_run_error import BetaManagedAgentsMemoryStoreArchivedRunError
from .beta_managed_agents_organization_disabled_run_error import BetaManagedAgentsOrganizationDisabledRunError
from .beta_managed_agents_session_creation_rejected_run_error import BetaManagedAgentsSessionCreationRejectedRunError
from .beta_managed_agents_session_resource_not_found_run_error import BetaManagedAgentsSessionResourceNotFoundRunError
from .beta_managed_agents_self_hosted_resources_unsupported_run_error import (
    BetaManagedAgentsSelfHostedResourcesUnsupportedRunError,
)

__all__ = ["BetaManagedAgentsDeploymentRun", "Error"]

Error: TypeAlias = Annotated[
    Union[
        BetaManagedAgentsEnvironmentArchivedRunError,
        BetaManagedAgentsAgentArchivedRunError,
        BetaManagedAgentsEnvironmentNotFoundRunError,
        BetaManagedAgentsVaultNotFoundRunError,
        BetaManagedAgentsVaultArchivedRunError,
        BetaManagedAgentsFileNotFoundRunError,
        BetaManagedAgentsMemoryStoreArchivedRunError,
        BetaManagedAgentsSkillNotFoundRunError,
        BetaManagedAgentsSessionResourceNotFoundRunError,
        BetaManagedAgentsWorkspaceArchivedRunError,
        BetaManagedAgentsOrganizationDisabledRunError,
        BetaManagedAgentsSessionRateLimitedRunError,
        BetaManagedAgentsSessionCreationRejectedRunError,
        BetaManagedAgentsUnknownRunError,
        BetaManagedAgentsSelfHostedResourcesUnsupportedRunError,
        BetaManagedAgentsMCPEgressBlockedRunError,
        None,
    ],
    PropertyInfo(discriminator="type"),
]


class BetaManagedAgentsDeploymentRun(BaseModel):
    """A persistent, append-only record of a single deployment execution.

    Records session creation success or failure — no session lifecycle tracking.
    """

    id: str
    """Unique identifier for this run (`drun_...`)."""

    agent: BetaManagedAgentsAgentReference
    """A resolved agent reference with a concrete version."""

    created_at: datetime
    """A timestamp in RFC 3339 format"""

    deployment_id: str
    """ID of the deployment that produced this run."""

    error: Optional[Error] = None
    """Why the run failed to create a session.

    The type identifies the failure; message is human-readable detail.
    """

    session_id: Optional[str] = None
    """Populated on success.

    Null on creation failure. Exactly one of session_id or error is non-null.
    """

    trigger_context: BetaManagedAgentsTriggerContext
    """Describes what triggered a deployment run, with trigger-specific metadata."""

    type: Literal["deployment_run"]
