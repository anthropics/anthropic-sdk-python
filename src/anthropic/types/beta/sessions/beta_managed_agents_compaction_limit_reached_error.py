from typing import Union
from typing_extensions import Literal, Annotated, TypeAlias

from ...._models import BaseModel, UnionDiscriminator
from .beta_managed_agents_retry_status_retrying import BetaManagedAgentsRetryStatusRetrying
from .beta_managed_agents_retry_status_terminal import BetaManagedAgentsRetryStatusTerminal
from .beta_managed_agents_retry_status_exhausted import BetaManagedAgentsRetryStatusExhausted

__all__ = ["BetaManagedAgentsCompactionLimitReachedError", "RetryStatus"]

RetryStatus: TypeAlias = Annotated[
    Union[
        BetaManagedAgentsRetryStatusRetrying,
        BetaManagedAgentsRetryStatusExhausted,
        BetaManagedAgentsRetryStatusTerminal,
    ],
    UnionDiscriminator("type"),
]


class BetaManagedAgentsCompactionLimitReachedError(BaseModel):
    """
    The turn stopped because the context was compacted the maximum number of times in a row without the model producing a message or a tool call, not because a request failed. The thread goes idle with `stop_reason: retries_exhausted` (a child thread then terminates); the next `user.message` starts a new turn.
    """

    message: str
    """Human-readable error description."""

    retry_status: RetryStatus
    """What the client should do next."""

    type: Literal["compaction_limit_reached_error"]
