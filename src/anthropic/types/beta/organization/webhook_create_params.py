from __future__ import annotations

from typing import List
from typing_extensions import Literal, Required, TypedDict

from ...anthropic_beta_param import AnthropicBetaParam

__all__ = ["WebhookCreateParams"]


class WebhookCreateParams(TypedDict, total=False):
    enabled_events: Required[
        List[Literal["user_profile.enforcement_action_opened", "user_profile.enforcement_action_resolved"]]
    ]
    """The event types to deliver to the endpoint. Must list at least one."""

    url: Required[str]
    """The HTTPS URL that deliveries are sent to."""

    description: str
    """Notes about the endpoint."""

    name: str
    """A short label for the endpoint."""

    betas: List[AnthropicBetaParam]
    """
    This endpoint is in beta: requests must send `webhooks-2026-10-07` in this
    header.
    """
