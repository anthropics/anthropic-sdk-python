from typing import List
from datetime import datetime
from typing_extensions import Literal

from ...._models import BaseModel
from .beta_organization_webhook_endpoint_state import BetaOrganizationWebhookEndpointState

__all__ = ["BetaOrganizationWebhookEndpoint"]


class BetaOrganizationWebhookEndpoint(BaseModel):
    """
    A webhook endpoint that belongs to the organization rather than to one of
    its workspaces.
    """

    id: str
    """ID of the webhook endpoint."""

    created_at: datetime
    """When the endpoint was created, in RFC 3339 format."""

    description: str
    """Notes about the endpoint. An empty string when none were given."""

    disabled_reason: str
    """Why Anthropic disabled the endpoint automatically.

    An empty string when the endpoint is enabled, or when you disabled it.
    """

    enabled_events: List[Literal["user_profile.enforcement_action_opened", "user_profile.enforcement_action_resolved"]]
    """The event types delivered to the endpoint."""

    name: str
    """A short label for the endpoint. An empty string when none was given."""

    state: BetaOrganizationWebhookEndpointState
    """Whether deliveries are sent to the endpoint."""

    updated_at: datetime
    """When the endpoint was last changed, in RFC 3339 format."""

    url: str
    """The HTTPS URL that deliveries are sent to."""
