from typing import Union
from datetime import datetime
from typing_extensions import Literal, Annotated, TypeAlias

from ...._models import BaseModel, UnionDiscriminator
from .beta_managed_agents_billing_error_object import BetaManagedAgentsBillingErrorObject
from .beta_managed_agents_unknown_error_object import BetaManagedAgentsUnknownErrorObject
from .beta_managed_agents_model_overloaded_error_object import BetaManagedAgentsModelOverloadedErrorObject
from .beta_managed_agents_repository_clone_error_object import BetaManagedAgentsRepositoryCloneErrorObject
from .beta_managed_agents_model_rate_limited_error_object import BetaManagedAgentsModelRateLimitedErrorObject
from .beta_managed_agents_repository_checkout_error_object import BetaManagedAgentsRepositoryCheckoutErrorObject
from .beta_managed_agents_model_request_failed_error_object import BetaManagedAgentsModelRequestFailedErrorObject
from .beta_managed_agents_repository_forbidden_error_object import BetaManagedAgentsRepositoryForbiddenErrorObject
from .beta_managed_agents_repository_not_found_error_object import BetaManagedAgentsRepositoryNotFoundErrorObject
from .beta_managed_agents_mcp_connection_failed_error_object import BetaManagedAgentsMCPConnectionFailedErrorObject
from .beta_managed_agents_tool_use_limit_reached_error_object import BetaManagedAgentsToolUseLimitReachedErrorObject
from .beta_managed_agents_compaction_limit_reached_error_object import (
    BetaManagedAgentsCompactionLimitReachedErrorObject,
)
from .beta_managed_agents_mcp_authentication_failed_error_object import (
    BetaManagedAgentsMCPAuthenticationFailedErrorObject,
)
from .beta_managed_agents_repository_authentication_error_object import (
    BetaManagedAgentsRepositoryAuthenticationErrorObject,
)
from .beta_managed_agents_credential_host_unreachable_error_object import (
    BetaManagedAgentsCredentialHostUnreachableErrorObject,
)

__all__ = ["BetaManagedAgentsSessionErrorEvent", "Error"]

Error: TypeAlias = Annotated[
    Union[
        BetaManagedAgentsUnknownErrorObject,
        BetaManagedAgentsModelOverloadedErrorObject,
        BetaManagedAgentsModelRateLimitedErrorObject,
        BetaManagedAgentsModelRequestFailedErrorObject,
        BetaManagedAgentsMCPConnectionFailedErrorObject,
        BetaManagedAgentsMCPAuthenticationFailedErrorObject,
        BetaManagedAgentsBillingErrorObject,
        BetaManagedAgentsCredentialHostUnreachableErrorObject,
        BetaManagedAgentsToolUseLimitReachedErrorObject,
        BetaManagedAgentsCompactionLimitReachedErrorObject,
        BetaManagedAgentsRepositoryAuthenticationErrorObject,
        BetaManagedAgentsRepositoryForbiddenErrorObject,
        BetaManagedAgentsRepositoryNotFoundErrorObject,
        BetaManagedAgentsRepositoryCheckoutErrorObject,
        BetaManagedAgentsRepositoryCloneErrorObject,
    ],
    UnionDiscriminator("type"),
]


class BetaManagedAgentsSessionErrorEvent(BaseModel):
    """An error event indicating a problem occurred during session execution."""

    id: str
    """Unique identifier for this event."""

    error: Error

    processed_at: datetime
    """Timestamp when the error occurred."""

    type: Literal["session.error"]
