from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaWebhookSessionStatusRescheduledEventData"]


class BetaWebhookSessionStatusRescheduledEventData(BaseModel):
    id: str
    """ID of the session that triggered the event."""

    organization_id: str

    type: Literal["session.status_rescheduled"]

    workspace_id: str
