# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Union
from typing_extensions import Annotated, TypeAlias

from ..._utils import PropertyInfo
from .beta_managed_agents_unknown_deployment_paused_reason_error import (
    BetaManagedAgentsUnknownDeploymentPausedReasonError,
)
from .beta_managed_agents_agent_archived_deployment_paused_reason_error import (
    BetaManagedAgentsAgentArchivedDeploymentPausedReasonError,
)
from .beta_managed_agents_file_not_found_deployment_paused_reason_error import (
    BetaManagedAgentsFileNotFoundDeploymentPausedReasonError,
)
from .beta_managed_agents_vault_archived_deployment_paused_reason_error import (
    BetaManagedAgentsVaultArchivedDeploymentPausedReasonError,
)
from .beta_managed_agents_skill_not_found_deployment_paused_reason_error import (
    BetaManagedAgentsSkillNotFoundDeploymentPausedReasonError,
)
from .beta_managed_agents_vault_not_found_deployment_paused_reason_error import (
    BetaManagedAgentsVaultNotFoundDeploymentPausedReasonError,
)
from .beta_managed_agents_mcp_egress_blocked_deployment_paused_reason_error import (
    BetaManagedAgentsMCPEgressBlockedDeploymentPausedReasonError,
)
from .beta_managed_agents_workspace_archived_deployment_paused_reason_error import (
    BetaManagedAgentsWorkspaceArchivedDeploymentPausedReasonError,
)
from .beta_managed_agents_environment_archived_deployment_paused_reason_error import (
    BetaManagedAgentsEnvironmentArchivedDeploymentPausedReasonError,
)
from .beta_managed_agents_environment_not_found_deployment_paused_reason_error import (
    BetaManagedAgentsEnvironmentNotFoundDeploymentPausedReasonError,
)
from .beta_managed_agents_memory_store_archived_deployment_paused_reason_error import (
    BetaManagedAgentsMemoryStoreArchivedDeploymentPausedReasonError,
)
from .beta_managed_agents_organization_disabled_deployment_paused_reason_error import (
    BetaManagedAgentsOrganizationDisabledDeploymentPausedReasonError,
)
from .beta_managed_agents_session_resource_not_found_deployment_paused_reason_error import (
    BetaManagedAgentsSessionResourceNotFoundDeploymentPausedReasonError,
)
from .beta_managed_agents_self_hosted_resources_unsupported_deployment_paused_reason_error import (
    BetaManagedAgentsSelfHostedResourcesUnsupportedDeploymentPausedReasonError,
)

__all__ = ["BetaManagedAgentsDeploymentPausedReasonError"]

BetaManagedAgentsDeploymentPausedReasonError: TypeAlias = Annotated[
    Union[
        BetaManagedAgentsEnvironmentArchivedDeploymentPausedReasonError,
        BetaManagedAgentsAgentArchivedDeploymentPausedReasonError,
        BetaManagedAgentsEnvironmentNotFoundDeploymentPausedReasonError,
        BetaManagedAgentsVaultNotFoundDeploymentPausedReasonError,
        BetaManagedAgentsFileNotFoundDeploymentPausedReasonError,
        BetaManagedAgentsSessionResourceNotFoundDeploymentPausedReasonError,
        BetaManagedAgentsWorkspaceArchivedDeploymentPausedReasonError,
        BetaManagedAgentsOrganizationDisabledDeploymentPausedReasonError,
        BetaManagedAgentsMemoryStoreArchivedDeploymentPausedReasonError,
        BetaManagedAgentsSkillNotFoundDeploymentPausedReasonError,
        BetaManagedAgentsVaultArchivedDeploymentPausedReasonError,
        BetaManagedAgentsUnknownDeploymentPausedReasonError,
        BetaManagedAgentsSelfHostedResourcesUnsupportedDeploymentPausedReasonError,
        BetaManagedAgentsMCPEgressBlockedDeploymentPausedReasonError,
    ],
    PropertyInfo(discriminator="type"),
]
