# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import TypedDict

__all__ = ["BetaManagedAgentsInjectionLocationUpdateParams"]


class BetaManagedAgentsInjectionLocationUpdateParams(TypedDict, total=False):
    """Updated injection location."""

    body: bool
    """Substitute when the placeholder appears in the request body."""

    header: bool
    """Substitute when the placeholder appears in a request header value."""
