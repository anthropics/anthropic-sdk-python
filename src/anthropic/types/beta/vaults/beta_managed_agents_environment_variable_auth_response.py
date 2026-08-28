# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Union
from typing_extensions import Literal, Annotated, TypeAlias

from ...._models import BaseModel, UnionDiscriminator
from .beta_managed_agents_injection_location_response import BetaManagedAgentsInjectionLocationResponse
from .beta_managed_agents_limited_credential_networking_response import (
    BetaManagedAgentsLimitedCredentialNetworkingResponse,
)
from .beta_managed_agents_unrestricted_credential_networking_response import (
    BetaManagedAgentsUnrestrictedCredentialNetworkingResponse,
)

__all__ = ["BetaManagedAgentsEnvironmentVariableAuthResponse", "Networking"]

Networking: TypeAlias = Annotated[
    Union[
        BetaManagedAgentsUnrestrictedCredentialNetworkingResponse, BetaManagedAgentsLimitedCredentialNetworkingResponse
    ],
    UnionDiscriminator("type"),
]


class BetaManagedAgentsEnvironmentVariableAuthResponse(BaseModel):
    """Environment variable credential details. The secret value is never returned."""

    injection_location: BetaManagedAgentsInjectionLocationResponse
    """Where in the outbound request the secret value is substituted."""

    networking: Networking
    """Outbound hosts the secret value is substituted on."""

    secret_name: str
    """Name of the environment variable."""

    type: Literal["environment_variable"]
