# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, List, Union, Iterable, Optional
from typing_extensions import Required, Annotated, TypeAlias, TypedDict

from ..._types import SequenceNotStr
from ..._utils import PropertyInfo
from ..anthropic_beta_param import AnthropicBetaParam
from .beta_managed_agents_agent_params import BetaManagedAgentsAgentParams
from .beta_managed_agents_schedule_params import BetaManagedAgentsScheduleParams
from .beta_managed_agents_file_resource_params import BetaManagedAgentsFileResourceParams
from .beta_managed_agents_memory_store_resource_param import BetaManagedAgentsMemoryStoreResourceParam
from .beta_managed_agents_deployment_initial_event_params import BetaManagedAgentsDeploymentInitialEventParams
from .beta_managed_agents_github_repository_resource_params import BetaManagedAgentsGitHubRepositoryResourceParams

__all__ = ["DeploymentCreateParams", "Agent", "Resource"]


class DeploymentCreateParams(TypedDict, total=False):
    agent: Required[Agent]
    """Agent to deploy.

    Accepts the `agent` ID string, which pins the latest version, or an `agent`
    object with both id and version specified. The agent must exist and not be
    archived.
    """

    environment_id: Required[str]
    """
    ID of the `environment` defining the container configuration for sessions
    created from this deployment.
    """

    initial_events: Required[Iterable[BetaManagedAgentsDeploymentInitialEventParams]]
    """Events to send to each session immediately after creation.

    At least 1, maximum 50.
    """

    name: Required[str]
    """Human-readable name for the deployment."""

    description: Optional[str]
    """Description of what the deployment does."""

    metadata: Dict[str, str]
    """Arbitrary key-value metadata.

    Maximum 16 pairs, keys up to 64 chars, values up to 512 chars.
    """

    resources: Iterable[Resource]
    """Resources (e.g.

    repositories, files) to mount into each session's container. Maximum 500.
    """

    schedule: Optional[BetaManagedAgentsScheduleParams]
    """5-field POSIX cron schedule.

    Literal wall-clock matching in the configured timezone.
    """

    vault_ids: SequenceNotStr[str]
    """
    Vault IDs for stored credentials the agent can use during sessions created from
    this deployment. Maximum 50.
    """

    betas: Annotated[List[AnthropicBetaParam], PropertyInfo(alias="anthropic-beta")]
    """Optional header to specify the beta version(s) you want to use."""


Agent: TypeAlias = Union[str, BetaManagedAgentsAgentParams]

Resource: TypeAlias = Union[
    BetaManagedAgentsGitHubRepositoryResourceParams,
    BetaManagedAgentsFileResourceParams,
    BetaManagedAgentsMemoryStoreResourceParam,
]
