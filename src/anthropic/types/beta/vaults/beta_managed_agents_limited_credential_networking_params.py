# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

from ...._types import SequenceNotStr

__all__ = ["BetaManagedAgentsLimitedCredentialNetworkingParams"]


class BetaManagedAgentsLimitedCredentialNetworkingParams(TypedDict, total=False):
    """Substitute the secret only on requests to the listed hosts."""

    allowed_hosts: Required[SequenceNotStr[str]]
    """Hostnames on which the secret will be substituted.

    Each entry is a bare hostname (`api.example.com`), an IPv4 address
    (`192.0.2.1`), or a `*.`-prefixed wildcard (`*.example.com`). URLs, ports,
    paths, and IPv6 addresses are not accepted. At most 16 entries.
    """

    type: Required[Literal["limited"]]
