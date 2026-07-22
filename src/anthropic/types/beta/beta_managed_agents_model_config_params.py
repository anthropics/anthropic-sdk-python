# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union, Optional
from typing_extensions import Literal, Required, TypeAlias, TypedDict

from .beta_managed_agents_model_param import BetaManagedAgentsModelParam
from .beta_managed_agents_effort_low_param import BetaManagedAgentsEffortLowParam
from .beta_managed_agents_effort_max_param import BetaManagedAgentsEffortMaxParam
from .beta_managed_agents_effort_high_param import BetaManagedAgentsEffortHighParam
from .beta_managed_agents_effort_xhigh_param import BetaManagedAgentsEffortXhighParam
from .beta_managed_agents_effort_medium_param import BetaManagedAgentsEffortMediumParam

__all__ = ["BetaManagedAgentsModelConfigParams", "Effort"]

Effort: TypeAlias = Union[
    Literal["low", "medium", "high", "xhigh", "max"],
    BetaManagedAgentsEffortLowParam,
    BetaManagedAgentsEffortMediumParam,
    BetaManagedAgentsEffortHighParam,
    BetaManagedAgentsEffortXhighParam,
    BetaManagedAgentsEffortMaxParam,
]


class BetaManagedAgentsModelConfigParams(TypedDict, total=False):
    """An object that defines additional configuration control over model use"""

    id: Required[BetaManagedAgentsModelParam]
    """The model that will power your agent.

    See [models](https://docs.anthropic.com/en/docs/models-overview) for additional
    details and options.
    """

    effort: Optional[Effort]
    """How hard Claude works on each inference call.

    Accepts a bare level string (`"high"`) or `{"type": "high"}`. On create,
    omitting it resolves the per-model default; on update, omitting it leaves the
    stored value unchanged.
    """

    speed: Optional[Literal["standard", "fast"]]
    """Inference speed mode.

    `fast` provides significantly faster output token generation at premium pricing.
    Not all models support `fast`; invalid combinations are rejected at create time.
    """
