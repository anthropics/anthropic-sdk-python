# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

from .beta_managed_agents_injection_location_params import BetaManagedAgentsInjectionLocationParams
from .beta_managed_agents_credential_networking_params import BetaManagedAgentsCredentialNetworkingParams

__all__ = ["BetaManagedAgentsEnvironmentVariableCreateParams"]


class BetaManagedAgentsEnvironmentVariableCreateParams(TypedDict, total=False):
    """Parameters for creating an environment variable credential."""

    networking: Required[BetaManagedAgentsCredentialNetworkingParams]
    """Outbound hosts the secret value is substituted on."""

    secret_name: Required[str]
    """Name of the environment variable. Immutable after create."""

    secret_value: Required[str]
    """Secret value. Write-only; never returned in responses."""

    type: Required[Literal["environment_variable"]]

    injection_location: BetaManagedAgentsInjectionLocationParams
    """Where in the outbound request the secret value may be substituted."""
