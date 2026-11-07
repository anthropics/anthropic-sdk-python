from __future__ import annotations

from typing_extensions import TypedDict

__all__ = ["BetaManagedAgentsInjectionLocationUpdateParams"]


class BetaManagedAgentsInjectionLocationUpdateParams(TypedDict, total=False):
    """Changes which parts of an outbound request the secret is substituted into.

    A location you leave out keeps its current setting.

    After the change, at least one location must be enabled.

    See [Authenticate with vaults](https://platform.claude.com/docs/en/managed-agents/vaults#add-a-credential) to learn more about injection locations.
    """

    body: bool
    """Substitute when the placeholder appears in the request body."""

    header: bool
    """Substitute when the placeholder appears in a request header value."""
