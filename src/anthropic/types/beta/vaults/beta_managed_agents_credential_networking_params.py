# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union
from typing_extensions import TypeAlias

from .beta_managed_agents_limited_credential_networking_params import BetaManagedAgentsLimitedCredentialNetworkingParams
from .beta_managed_agents_unrestricted_credential_networking_params import (
    BetaManagedAgentsUnrestrictedCredentialNetworkingParams,
)

__all__ = ["BetaManagedAgentsCredentialNetworkingParams"]

BetaManagedAgentsCredentialNetworkingParams: TypeAlias = Union[
    BetaManagedAgentsUnrestrictedCredentialNetworkingParams, BetaManagedAgentsLimitedCredentialNetworkingParams
]
