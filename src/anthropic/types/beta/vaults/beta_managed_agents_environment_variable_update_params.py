# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Literal, Required, TypedDict

from .beta_managed_agents_credential_networking_params import BetaManagedAgentsCredentialNetworkingParams
from .beta_managed_agents_injection_location_update_params import BetaManagedAgentsInjectionLocationUpdateParams

__all__ = ["BetaManagedAgentsEnvironmentVariableUpdateParams"]


class BetaManagedAgentsEnvironmentVariableUpdateParams(TypedDict, total=False):
    """Parameters for updating an environment variable credential.

    `secret_name` is immutable.
    """

    type: Required[Literal["environment_variable"]]

    injection_location: BetaManagedAgentsInjectionLocationUpdateParams
    """Updated injection location."""

    networking: Optional[BetaManagedAgentsCredentialNetworkingParams]
    """Updated networking scope. Full replacement."""

    secret_value: Optional[str]
    """Updated secret value."""
