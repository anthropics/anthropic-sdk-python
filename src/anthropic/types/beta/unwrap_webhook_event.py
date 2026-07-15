# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from datetime import datetime
from typing_extensions import Literal

from ..._models import BaseModel
from .beta_webhook_event_data import BetaWebhookEventData

__all__ = ["UnwrapWebhookEvent"]


class UnwrapWebhookEvent(BaseModel):
    id: str
    """Unique event identifier for idempotency."""

    created_at: datetime
    """RFC 3339 timestamp when the event occurred."""

    data: BetaWebhookEventData

    type: Literal["event"]
    """Object type. Always `event` for webhook payloads."""
