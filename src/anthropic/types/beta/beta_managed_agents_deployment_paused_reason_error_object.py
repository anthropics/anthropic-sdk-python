from typing import Union
from typing_extensions import Annotated, TypeAlias

from ..._models import UnionDiscriminator
from .beta_managed_agents_unknown_deployment_paused_reason_error_object import (
    BetaManagedAgentsUnknownDeploymentPausedReasonErrorObject,
)
from .beta_managed_agents_agent_archived_deployment_paused_reason_error_object import (
    BetaManagedAgentsAgentArchivedDeploymentPausedReasonErrorObject,
)
from .beta_managed_agents_file_not_found_deployment_paused_reason_error_object import (
    BetaManagedAgentsFileNotFoundDeploymentPausedReasonErrorObject,
)
from .beta_managed_agents_vault_archived_deployment_paused_reason_error_object import (
    BetaManagedAgentsVaultArchivedDeploymentPausedReasonErrorObject,
)
from .beta_managed_agents_skill_not_found_deployment_paused_reason_error_object import (
    BetaManagedAgentsSkillNotFoundDeploymentPausedReasonErrorObject,
)
from .beta_managed_agents_vault_not_found_deployment_paused_reason_error_object import (
    BetaManagedAgentsVaultNotFoundDeploymentPausedReasonErrorObject,
)
from .beta_managed_agents_mcp_egress_blocked_deployment_paused_reason_error_object import (
    BetaManagedAgentsMCPEgressBlockedDeploymentPausedReasonErrorObject,
)
from .beta_managed_agents_workspace_archived_deployment_paused_reason_error_object import (
    BetaManagedAgentsWorkspaceArchivedDeploymentPausedReasonErrorObject,
)
from .beta_managed_agents_environment_archived_deployment_paused_reason_error_object import (
    BetaManagedAgentsEnvironmentArchivedDeploymentPausedReasonErrorObject,
)
from .beta_managed_agents_environment_not_found_deployment_paused_reason_error_object import (
    BetaManagedAgentsEnvironmentNotFoundDeploymentPausedReasonErrorObject,
)
from .beta_managed_agents_memory_store_archived_deployment_paused_reason_error_object import (
    BetaManagedAgentsMemoryStoreArchivedDeploymentPausedReasonErrorObject,
)
from .beta_managed_agents_organization_disabled_deployment_paused_reason_error_object import (
    BetaManagedAgentsOrganizationDisabledDeploymentPausedReasonErrorObject,
)
from .beta_managed_agents_session_resource_not_found_deployment_paused_reason_error_object import (
    BetaManagedAgentsSessionResourceNotFoundDeploymentPausedReasonErrorObject,
)
from .beta_managed_agents_self_hosted_resources_unsupported_deployment_paused_reason_error_object import (
    BetaManagedAgentsSelfHostedResourcesUnsupportedDeploymentPausedReasonErrorObject,
)

__all__ = ["BetaManagedAgentsDeploymentPausedReasonErrorObject"]

BetaManagedAgentsDeploymentPausedReasonErrorObject: TypeAlias = Annotated[
    Union[
        BetaManagedAgentsEnvironmentArchivedDeploymentPausedReasonErrorObject,
        BetaManagedAgentsAgentArchivedDeploymentPausedReasonErrorObject,
        BetaManagedAgentsEnvironmentNotFoundDeploymentPausedReasonErrorObject,
        BetaManagedAgentsVaultNotFoundDeploymentPausedReasonErrorObject,
        BetaManagedAgentsFileNotFoundDeploymentPausedReasonErrorObject,
        BetaManagedAgentsSessionResourceNotFoundDeploymentPausedReasonErrorObject,
        BetaManagedAgentsWorkspaceArchivedDeploymentPausedReasonErrorObject,
        BetaManagedAgentsOrganizationDisabledDeploymentPausedReasonErrorObject,
        BetaManagedAgentsMemoryStoreArchivedDeploymentPausedReasonErrorObject,
        BetaManagedAgentsSkillNotFoundDeploymentPausedReasonErrorObject,
        BetaManagedAgentsVaultArchivedDeploymentPausedReasonErrorObject,
        BetaManagedAgentsUnknownDeploymentPausedReasonErrorObject,
        BetaManagedAgentsSelfHostedResourcesUnsupportedDeploymentPausedReasonErrorObject,
        BetaManagedAgentsMCPEgressBlockedDeploymentPausedReasonErrorObject,
    ],
    UnionDiscriminator("type"),
]
"""The error that triggered an auto-pause. Matches the failed run's `error.type`."""
