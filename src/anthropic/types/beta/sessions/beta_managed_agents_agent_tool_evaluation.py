from typing import Union
from typing_extensions import Annotated, TypeAlias

from ...._models import UnionDiscriminator
from .beta_managed_agents_agent_tool_evaluation_auto import BetaManagedAgentsAgentToolEvaluationAuto
from .beta_managed_agents_agent_tool_evaluation_always_ask import BetaManagedAgentsAgentToolEvaluationAlwaysAsk
from .beta_managed_agents_agent_tool_evaluation_always_allow import BetaManagedAgentsAgentToolEvaluationAlwaysAllow

__all__ = ["BetaManagedAgentsAgentToolEvaluation"]

BetaManagedAgentsAgentToolEvaluation: TypeAlias = Annotated[
    Union[
        BetaManagedAgentsAgentToolEvaluationAlwaysAllow,
        BetaManagedAgentsAgentToolEvaluationAlwaysAsk,
        BetaManagedAgentsAgentToolEvaluationAuto,
    ],
    UnionDiscriminator("type"),
]
