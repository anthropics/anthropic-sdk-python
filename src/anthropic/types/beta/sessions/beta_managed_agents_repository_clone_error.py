from typing import Union, Optional
from typing_extensions import Literal, Annotated, TypeAlias

from ...._models import BaseModel, UnionDiscriminator
from .beta_managed_agents_retry_status_retrying import BetaManagedAgentsRetryStatusRetrying
from .beta_managed_agents_retry_status_terminal import BetaManagedAgentsRetryStatusTerminal
from .beta_managed_agents_retry_status_exhausted import BetaManagedAgentsRetryStatusExhausted

__all__ = ["BetaManagedAgentsRepositoryCloneError", "RetryStatus"]

RetryStatus: TypeAlias = Annotated[
    Union[
        BetaManagedAgentsRetryStatusRetrying,
        BetaManagedAgentsRetryStatusExhausted,
        BetaManagedAgentsRetryStatusTerminal,
    ],
    UnionDiscriminator("type"),
]


class BetaManagedAgentsRepositoryCloneError(BaseModel):
    """The repository could not be cloned."""

    message: str
    """Human-readable error description."""

    repository_url: Optional[str] = None
    """URL of the repository that could not be cloned.

    Null when it could not be identified.
    """

    retry_status: RetryStatus
    """What the client should do next.

    Always `retrying`: the session keeps running without the repository.
    """

    type: Literal["repository_clone_error"]
