# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Union
from typing_extensions import Literal, Annotated, TypeAlias

from ...._utils import PropertyInfo
from ...._models import BaseModel
from .beta_managed_agents_retry_status_retrying import BetaManagedAgentsRetryStatusRetrying
from .beta_managed_agents_retry_status_terminal import BetaManagedAgentsRetryStatusTerminal
from .beta_managed_agents_retry_status_exhausted import BetaManagedAgentsRetryStatusExhausted

__all__ = ["BetaManagedAgentsCredentialHostUnreachableError", "RetryStatus"]

RetryStatus: TypeAlias = Annotated[
    Union[
        BetaManagedAgentsRetryStatusRetrying,
        BetaManagedAgentsRetryStatusExhausted,
        BetaManagedAgentsRetryStatusTerminal,
    ],
    PropertyInfo(discriminator="type"),
]


class BetaManagedAgentsCredentialHostUnreachableError(BaseModel):
    """
    An `environment_variable` credential's `auth.networking.allowed_hosts` includes a host the environment's network policy does not permit.
    """

    credential_id: str
    """ID of the affected credential."""

    message: str
    """Human-readable error description."""

    retry_status: RetryStatus
    """What the client should do next in response to this error."""

    type: Literal["credential_host_unreachable_error"]

    vault_id: str
    """ID of the vault containing the affected credential."""
