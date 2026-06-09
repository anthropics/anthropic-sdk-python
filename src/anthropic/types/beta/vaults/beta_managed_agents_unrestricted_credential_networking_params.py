# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["BetaManagedAgentsUnrestrictedCredentialNetworkingParams"]


class BetaManagedAgentsUnrestrictedCredentialNetworkingParams(TypedDict, total=False):
    """
    Substitute the secret on any host the session's Environment network policy permits egress to. The Environment's network policy is the only boundary on where the secret can reach.
    """

    type: Required[Literal["unrestricted"]]
