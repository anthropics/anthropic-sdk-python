# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from ..._models import BaseModel
from .beta_webhook_environment_deleted_event_type import BetaWebhookEnvironmentDeletedEventType

__all__ = ["BetaWebhookEnvironmentDeletedEventData"]


class BetaWebhookEnvironmentDeletedEventData(BaseModel):
    id: str
    """ID of the environment that triggered the event."""

    organization_id: str

    type: BetaWebhookEnvironmentDeletedEventType

    workspace_id: str
