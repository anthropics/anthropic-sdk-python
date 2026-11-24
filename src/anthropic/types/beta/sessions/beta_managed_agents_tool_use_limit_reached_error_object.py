from typing import Union
from typing_extensions import Literal, Annotated, TypeAlias

from ...._models import BaseModel, UnionDiscriminator
from .beta_managed_agents_retry_status_retrying import BetaManagedAgentsRetryStatusRetrying
from .beta_managed_agents_retry_status_terminal import BetaManagedAgentsRetryStatusTerminal
from .beta_managed_agents_retry_status_exhausted import BetaManagedAgentsRetryStatusExhausted

__all__ = ["BetaManagedAgentsToolUseLimitReachedErrorObject", "RetryStatus"]

RetryStatus: TypeAlias = Annotated[
    Union[
        BetaManagedAgentsRetryStatusRetrying,
        BetaManagedAgentsRetryStatusExhausted,
        BetaManagedAgentsRetryStatusTerminal,
    ],
    UnionDiscriminator("type"),
]
"""What the client should do next."""


class BetaManagedAgentsToolUseLimitReachedErrorObject(BaseModel):
    """The turn stopped at one of two limits on tool use, not because a request failed.

    One limit is on tool-use rounds (one model response that calls tools, plus running those tools, is one round). The other is on model responses in a row that each request a single tool call and are cut off by the model's output or context limit before the call is complete. None of those calls runs. `message` states the limit that applied. The thread goes idle with `stop_reason: retries_exhausted` (a child thread then terminates); the next `user.message` starts a new turn.
    """

    message: str
    """Human-readable error description."""

    retry_status: RetryStatus
    """What the client should do next."""

    type: Literal["tool_use_limit_reached_error"]
