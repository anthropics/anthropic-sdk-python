from __future__ import annotations

from typing import Optional
from typing_extensions import Literal, Required, TypedDict

from .beta_managed_agents_multiagent_advisor_params import BetaManagedAgentsMultiagentAdvisorParams
from .beta_managed_agents_multiagent_subagents_params import BetaManagedAgentsMultiagentSubagentsParams
from .beta_managed_agents_multiagent_workflows_params import BetaManagedAgentsMultiagentWorkflowsParams

__all__ = ["BetaManagedAgentsMultiagent20261001Params"]


class BetaManagedAgentsMultiagent20261001Params(TypedDict, total=False):
    """Multiagent configuration with three members, each enabled or disabled on its own.

    On an update, if the agent's stored `multiagent` also has type `multiagent_20261001`, this configuration is merged into the stored one, level by level, instead of replacing it. A key that the update omits keeps its stored value. A key sent as null takes its default, on create as well, so `"workflows": null` enables workflows. An object sent with a `type` other than the stored one replaces the stored object, and the keys that it omits take their defaults. A `predefined_agents` list that is sent replaces the stored list. Every object that is sent needs its `type`, and an enabled `advisor` needs its `model`. Other validation applies to the merged result.
    """

    type: Required[Literal["multiagent_20261001"]]

    advisor: Optional[BetaManagedAgentsMultiagentAdvisorParams]
    """Whether the session's primary thread can consult an advisor model.

    Defaults to disabled.
    """

    subagents: Optional[BetaManagedAgentsMultiagentSubagentsParams]
    """Whether the agent can spawn session threads. Defaults to enabled."""

    workflows: Optional[BetaManagedAgentsMultiagentWorkflowsParams]
    """Whether the agent can start workflow runs. Defaults to enabled."""
