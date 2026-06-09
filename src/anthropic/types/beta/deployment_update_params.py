# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, List, Union, Iterable, Optional
from typing_extensions import Annotated, TypeAlias, TypedDict

from ..._types import SequenceNotStr
from ..._utils import PropertyInfo
from ..anthropic_beta_param import AnthropicBetaParam
from .beta_managed_agents_agent_params import BetaManagedAgentsAgentParams
from .beta_managed_agents_schedule_params import BetaManagedAgentsScheduleParams
from .beta_managed_agents_file_resource_params import BetaManagedAgentsFileResourceParams
from .beta_managed_agents_memory_store_resource_param import BetaManagedAgentsMemoryStoreResourceParam
from .beta_managed_agents_deployment_initial_event_params import BetaManagedAgentsDeploymentInitialEventParams
from .beta_managed_agents_github_repository_resource_params import BetaManagedAgentsGitHubRepositoryResourceParams

__all__ = ["DeploymentUpdateParams", "Agent", "Resource"]


class DeploymentUpdateParams(TypedDict, total=False):
    agent: Agent
    """Agent to deploy.

    Accepts the `agent` ID string, which re-pins to the latest version, or an
    `agent` object with both id and version specified. Omit to preserve. Cannot be
    cleared.
    """

    description: Optional[str]
    """Description. Omit to preserve; send empty string or null to clear."""

    environment_id: str
    """ID of the `environment` where sessions run.

    Omit to preserve. Cannot be cleared.
    """

    initial_events: Iterable[BetaManagedAgentsDeploymentInitialEventParams]
    """Initial events.

    Full replacement. Omit to preserve. Cannot be cleared. At least 1, maximum 50.
    """

    metadata: Optional[Dict[str, Optional[str]]]
    """Metadata patch.

    Set a key to a string to upsert it, or to null to delete it. Omit the field to
    preserve. The stored bag is limited to 16 keys (up to 64 chars each) with values
    up to 512 chars.
    """

    name: str
    """Human-readable name. Must be non-empty. Omit to preserve. Cannot be cleared."""

    resources: Optional[Iterable[Resource]]
    """Session resources.

    Full replacement. Omit to preserve; send empty array or null to clear.
    Maximum 500.
    """

    schedule: Optional[BetaManagedAgentsScheduleParams]
    """5-field POSIX cron schedule.

    Literal wall-clock matching in the configured timezone.
    """

    vault_ids: Optional[SequenceNotStr[str]]
    """Vault IDs.

    Full replacement. Omit to preserve; send empty array or null to clear.
    Maximum 50.
    """

    betas: Annotated[List[AnthropicBetaParam], PropertyInfo(alias="anthropic-beta")]
    """Optional header to specify the beta version(s) you want to use."""


Agent: TypeAlias = Union[str, BetaManagedAgentsAgentParams]

Resource: TypeAlias = Union[
    BetaManagedAgentsGitHubRepositoryResourceParams,
    BetaManagedAgentsFileResourceParams,
    BetaManagedAgentsMemoryStoreResourceParam,
]
