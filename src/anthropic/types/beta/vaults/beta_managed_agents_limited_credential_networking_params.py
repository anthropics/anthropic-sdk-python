from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

from ...._types import SequenceNotStr

__all__ = ["BetaManagedAgentsLimitedCredentialNetworkingParams"]


class BetaManagedAgentsLimitedCredentialNetworkingParams(TypedDict, total=False):
    """Substitute the secret only on requests to the listed hosts."""

    allowed_hosts: Required[SequenceNotStr[str]]
    """
    The destination hosts of the outbound requests that the credential's secret is
    substituted into.

    Each entry is a bare hostname (`api.example.com`), an IPv4 address
    (`192.0.2.1`), or a `*.` wildcard (`*.example.com`). URLs, ports, paths, and
    IPv6 addresses aren't accepted. The list can have up to 16 entries.
    """

    type: Required[Literal["limited"]]
