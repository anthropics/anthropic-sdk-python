from __future__ import annotations

from typing import Dict, List, Union, Iterable, Optional
from typing_extensions import Required, TypeAlias, TypedDict

from ..._types import SequenceNotStr
from ..anthropic_beta_param import AnthropicBetaParam
from .beta_managed_agents_agent_params import BetaManagedAgentsAgentParams
from .beta_managed_agents_schedule_params import BetaManagedAgentsScheduleParams
from .beta_managed_agents_budget_limit_param import BetaManagedAgentsBudgetLimitParam
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

    budget: Optional[BetaManagedAgentsBudgetLimitParam]
    """
    Enforced spend ceiling stamped onto each session created from this deployment,
    copied at session-creation time. Omit to leave sessions uncapped. The deployment
    agent's model must have a public list price, or the request is rejected; a
    multiagent roster is re-validated in full when each fire copies the cap, which
    fails closed the same way.
    """

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
    """Optional recurring cron schedule.

    When present, the deployment fires automatically. Both expression and timezone
    are required when schedule is set.
    """

    vault_ids: SequenceNotStr[str]
    """
    Vault IDs for stored credentials the agent can use during sessions created from
    this deployment. Maximum 50.
    """

    betas: List[AnthropicBetaParam]
    """Optional header to specify the beta version(s) you want to use."""

    workspace_id: str
    """Optional header to select the Workspace for this request.

    The value is a Workspace ID (for example, `wrkspc_011CZkZaBF1tNoB5wlCeusgy`).

    Only needed for credentials that can act on more than one Workspace. A
    credential that belongs to a specific Workspace may omit it; if sent, it must
    match that Workspace.
    """


Agent: TypeAlias = Union[str, BetaManagedAgentsAgentParams]

Resource: TypeAlias = Union[
    BetaManagedAgentsGitHubRepositoryResourceParams,
    BetaManagedAgentsFileResourceParams,
    BetaManagedAgentsMemoryStoreResourceParam,
]
