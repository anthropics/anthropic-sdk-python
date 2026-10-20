from __future__ import annotations

from typing import List
from typing_extensions import Literal, TypedDict

from ...anthropic_beta_param import AnthropicBetaParam

__all__ = ["WebhookUpdateParams"]


class WebhookUpdateParams(TypedDict, total=False):
    description: str
    """Notes about the endpoint."""

    enabled_events: List[Literal["user_profile.enforcement_action_opened", "user_profile.enforcement_action_resolved"]]
    """The event types to deliver to the endpoint.

    Replaces the whole set; an empty list leaves it unchanged.
    """

    name: str
    """A short label for the endpoint."""

    state: Literal["disabled", "enabled"]
    """`disabled` stops deliveries.

    `enabled` resumes them and clears `disabled_reason`. Events that happen while
    the endpoint is disabled are never delivered.
    """

    url: str
    """The HTTPS URL that deliveries are sent to."""

    betas: List[AnthropicBetaParam]
    """
    This endpoint is in beta: requests must send `webhooks-2026-10-07` in this
    header.
    """
