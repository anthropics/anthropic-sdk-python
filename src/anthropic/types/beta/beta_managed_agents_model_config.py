# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Union, Optional
from typing_extensions import Literal, Annotated, TypeAlias

from ..._utils import PropertyInfo
from ..._models import BaseModel
from .beta_managed_agents_model import BetaManagedAgentsModel
from .beta_managed_agents_effort_low import BetaManagedAgentsEffortLow
from .beta_managed_agents_effort_max import BetaManagedAgentsEffortMax
from .beta_managed_agents_effort_high import BetaManagedAgentsEffortHigh
from .beta_managed_agents_effort_xhigh import BetaManagedAgentsEffortXhigh
from .beta_managed_agents_effort_medium import BetaManagedAgentsEffortMedium

__all__ = ["BetaManagedAgentsModelConfig", "Effort"]

Effort: TypeAlias = Annotated[
    Union[
        BetaManagedAgentsEffortLow,
        BetaManagedAgentsEffortMedium,
        BetaManagedAgentsEffortHigh,
        BetaManagedAgentsEffortXhigh,
        BetaManagedAgentsEffortMax,
    ],
    PropertyInfo(discriminator="type"),
]


class BetaManagedAgentsModelConfig(BaseModel):
    """Model identifier and configuration."""

    id: BetaManagedAgentsModel
    """The model that will power your agent.

    See [models](https://docs.anthropic.com/en/docs/models-overview) for additional
    details and options.
    """

    effort: Optional[Effort] = None
    """How hard Claude works on each turn.

    Sets `output_config.effort` on every Messages call the session makes.
    """

    speed: Optional[Literal["standard", "fast"]] = None
    """Inference speed mode.

    `fast` provides significantly faster output token generation at premium pricing.
    Not all models support `fast`; invalid combinations are rejected at create time.
    """
