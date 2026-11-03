from typing import Union
from typing_extensions import Literal, Annotated, TypeAlias

from ...._models import BaseModel, UnionDiscriminator
from .beta_managed_agents_retry_status_retrying import BetaManagedAgentsRetryStatusRetrying
from .beta_managed_agents_retry_status_terminal import BetaManagedAgentsRetryStatusTerminal
from .beta_managed_agents_retry_status_exhausted import BetaManagedAgentsRetryStatusExhausted

__all__ = ["BetaManagedAgentsToolUseLimitReachedError", "RetryStatus"]

RetryStatus: TypeAlias = Annotated[
    Union[
        BetaManagedAgentsRetryStatusRetrying,
        BetaManagedAgentsRetryStatusExhausted,
        BetaManagedAgentsRetryStatusTerminal,
    ],
    UnionDiscriminator("type"),
]


class BetaManagedAgentsToolUseLimitReachedError(BaseModel):
    """
    The turn stopped because the agent loop reached its limit on tool-use rounds (one model response that calls tools, plus running those tools, is one round), not because a request failed. The thread goes idle with `stop_reason: retries_exhausted` (a child thread then terminates); the next `user.message` starts a new turn.
    """

    message: str
    """Human-readable error description."""

    retry_status: RetryStatus
    """What the client should do next."""

    type: Literal["tool_use_limit_reached_error"]
