from typing_extensions import Literal, TypeAlias

__all__ = ["BetaOrganizationWebhookEndpointState"]

BetaOrganizationWebhookEndpointState: TypeAlias = Literal["disabled", "enabled"]
"""Whether deliveries are sent to an organization webhook endpoint."""
