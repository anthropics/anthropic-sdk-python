from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["BetaManagedAgentsServiceAccountExecutionIdentityParams"]


class BetaManagedAgentsServiceAccountExecutionIdentityParams(TypedDict, total=False):
    """The Anthropic-managed service account — the default execution principal.

    Carries no identifier.
    """

    type: Required[Literal["service_account"]]
